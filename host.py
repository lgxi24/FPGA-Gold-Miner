import time
import intel_jtag_uart
import sys


try:
    ju = intel_jtag_uart.intel_jtag_uart()
    # ju.get_info()
    
except Exception as e:
    print(e)
    sys.exit(0)
    
    
# time.sleep(1)

buffer = ""  # Initialize an empty buffer to accumulate data
def user_write(user_input):
    command = "nios2-terminal <<< {}".format(user_input)
    byte_object = command.encode('utf-8')
    ju.write(byte_object)
    
while True:
    # time.sleep(0.1)
    reading = ju.read()
    # user_input = input("Score: ")
    
    if reading:  # If there's data read from the UART
        # if user_input:
        #     user_write(user_input)
        # print('a')    
        buffer += reading.decode('utf-8')  # Append the data to the buffer, decode if necessary
        
        # Check if there are at least two newline characters in the buffer
        if buffer.count('\n') >= 2:
            # Find the position of the first two newline characters
            first_newline_pos = buffer.find('\n')
            second_newline_pos = buffer.find('\n', first_newline_pos + 1)
            
            # Extract the content between the first two newline characters
            content_between_newlines = buffer[first_newline_pos+1:second_newline_pos]
            for i in range (50):
                if i==49:
                    # print("read: ", content_between_newlines)
                    if content_between_newlines[0] == 'r':
                        print(content_between_newlines)
                        with open('output.txt', 'w') as file:
                            file.write(content_between_newlines)
                    buffer = buffer[second_newline_pos+1:]
                        # Remove the processed part from the buffer, including the second newline
                    i=0
                buffer = buffer[second_newline_pos+1:]
                i=i+1
            
  

           
