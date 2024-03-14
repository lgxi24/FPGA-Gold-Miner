import socket
import threading
import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('PlayerScores')  

player_data = {}
condition = threading.Condition()

def flush_all_records():
    table = dynamodb.Table('players')
    try:
        response = table.scan()
        items = response.get('Items', [])
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
            
        for item in items:
            player_id = item['player_id']
            table.delete_item(Key={'player_id': player_id})
        
        print("All records have been flushed from the 'players' table.")
    except Exception as e:
        print(f"Error flushing records: {e}")

def send_message(conn, message):
    try:
        conn.sendall(message)
    except Exception as e:
        print(f"Error sending message: {e}")

def write_player_to_json(players):
    modified_players = []
    for player in players:
        modified_player = {key: (float(value) if isinstance(value, Decimal) else value) for key, value in player.items()}
        modified_players.append(modified_player)
    return json.dumps(modified_players, indent=4)

def create_player_table():
    try:
        table = dynamodb.create_table(
            TableName='players',
            KeySchema=[{'AttributeName': 'player_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'player_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='players')
        print("Table created successfully.")
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("Table already exists.")

def load_player(players):
    table = dynamodb.Table('players')
    for player in players:
        player_id = player['player_id']
        print("Adding or updating player:", player_id)
        try:
            response = table.get_item(Key={'player_id': player_id})
        except Exception as e:
            print(f"Error retrieving player {player_id}: {e}")
            continue

        existing_player = response.get('Item')
        if existing_player:
            existing_score = existing_player['score']
            new_score = player['score']
            if new_score > existing_score:
                try:
                    table.put_item(Item=player)
                    print(f"Updated player {player_id} with higher score.")
                except Exception as e:
                    print(f"Error updating player {player_id}: {e}")
            else:
                print(f"Player {player_id} already has equal or higher score. No update needed.")
        else:
            try:
                table.put_item(Item=player)
                print(f"Inserted new player {player_id}.")
            except Exception as e:
                print(f"Error inserting player {player_id}: {e}")

def get_ranked_scores():
    table = dynamodb.Table('players')
    response = table.scan()
    items = response.get('Items', [])
    ranked_scores = sorted(items, key=lambda x: x['score'], reverse=True)

    return ranked_scores

def handle_client_request(conn, addr):
    global player_data
    
    player_ip = addr[0]  
    print(f"Connected by {addr}, Player IP: {player_ip}") 

    data = conn.recv(1024)
    if not data:
        conn.close()
        return

    if data.decode() == "get rank":
        ranked_scores = get_ranked_scores()
        ranked_scores = write_player_to_json(ranked_scores)
        scores_message = ranked_scores.encode()
        send_message(conn, scores_message)
    else:
        try:
            score = int(data.decode('utf-8'))
            print(f"Received score {score} from Player IP {player_ip}")
            player = [{'player_id': str(player_ip), 'score': score}]
            load_player(player)

            with condition:
                player_data[player_ip] = {'score': score, 'conn': conn}

                if len(player_data) == 1:
                    send_message(conn, b"Waiting for the other player's result...")

                if len(player_data) == 2:
                    condition.notify_all()
                else:
                    condition.wait()

            if len(player_data) == 2:
                winner_ip = max(player_data, key=lambda ip: player_data[ip]['score'])
                for ip, data in player_data.items():
                    message = b"You win!" if ip == winner_ip else b"You lose."
                    send_message(data['conn'], message)
                    data['conn'].close()

                with condition:
                    player_data.clear()
        except ValueError:
            print(f"Received non-integer data from Player IP {player_ip}")

def start_server(host, port):
    create_player_table()
    players = [{'player_id': '192.168.1.1', 'score': 1700},
    {'player_id': '192.168.1.2', 'score': 2030},{'player_id': '192.168.1.2', 'score': 1030}]
    load_player(players)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            try:
                conn, addr = s.accept()

                client_thread = threading.Thread(target=handle_client_request, args=(conn, addr))
                client_thread.start()
            except Exception as e:
                print(f"Server error: {e}")

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 12000       
    # flush_all_records()
    start_server(HOST, PORT)
