import time
import intel_jtag_uart
import sys


try:
    ju = intel_jtag_uart.intel_jtag_uart()
    # ju.get_info()
    
except Exception as e:
    print(e)
    sys.exit(0)

# read from 
with open('input.txt', 'r') as file:
    last_content = file.read()  # Initialize the last read content

buffer = ""  # Initialize an empty buffer to accumulate data
# def user_write(user_input):
#     command = "nios2-terminal <<< {}".format(user_input)
#     byte_object = command.encode('utf-8')
#     ju.write(byte_object)
    
while True:
    # time.sleep(0.1)
    reading = ju.read()
    # user_input = input("Score: ")

    # read score from input.txt   
    
    if reading:  # If there's data read from the UART 
        # with open('input.txt', 'r') as file:
        #     content = file.read()  # Read the current content
        # score = int(content.strip())  # Assuming content is a number
        # ju.write(f"{score}\n".encode('utf-8'))  # Write the content into ju.write
        # ju.write(f"{1}\n".encode('utf-8'))

        buffer += reading.decode('utf-8')  # Append the data to the buffer, decode if necessary
        
        # Check if there are at least two newline characters in the buffer
        if buffer.count('\n') >= 2:
            # Find the position of the first two newline characters
            first_newline_pos = buffer.find('\n')
            second_newline_pos = buffer.find('\n', first_newline_pos + 1)
            
            # Extract the content between the first two newline characters
            content_between_newlines = buffer[first_newline_pos+1:second_newline_pos]
            for i in range (201):
                
                if i%49==0:
                    # print("read: ", content_between_newlines)
                    if content_between_newlines[0] == 'r':
                        # print(content_between_newlines)
                        with open('output.txt', 'w') as file:
                            file.write(content_between_newlines)       
                    buffer = buffer[second_newline_pos+1:]
                    
                        # Remove the processed part from the buffer, including the second newline
                if i==200:
                    # print("write to led")
                    with open('input.txt', 'r') as file:
                        content = file.read()  # Read the current content
                    if content:
                        score = int(content.strip())  # Assuming content is a number
                        ju.write(f"{score}\n".encode('utf-8'))  # Write the content into ju.write    
                    i=0
                # print(i)
                buffer = buffer[second_newline_pos+1:]
                i=i+1
            
  

           
