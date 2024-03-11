#include <sys/alt_stdio.h>
#include <stdio.h>
#include "altera_avalon_pio_regs.h"
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "sys/alt_irq.h"
#include <stdlib.h>

// define for seven segment display
#define CHARLIM 256	//Maximum character length of what the user places in memory.  Increase to allow longer sequences
#define CLOCKINIT 30005	//Initial speed of the display.  This is a good starting point

// define for accelerometer
#define OFFSET -32
#define PWM_PERIOD 16
#define N_TAPS 5

// predefine all the functions
void updateText();			//Updates the text from the console once the program is running
char getTxt(char curr);		//Gets the text the user placed on the console
int getActualText();		//Takes the user's input and only uses the allowed letters.  Returns the length of the string entered
void clearActualText();		//This function clears the text on the display
int getBin(char letter);		//Gets the binary representation of the character
void print(int let5, int let4, int let3, int let2, int let1, int let0);	//Prints each of the letters out to the screen
void SevenSegmentDisplay();	//Main function that runs the display
void led_write(alt_u8 accelerometer_pattern, int button_datain);
void convert_read(alt_32 acc_read, int * level, alt_u8 * led);
float apply_filter(alt_32 new_reading);
void sys_timer_isr();
int button_display();




// initialisation for seven segment display
char prevLetter;	//The last letter the user entered, used for determining whether or not the display has been updated
char enteredText[CHARLIM]; //The text that the user enters
char text[2*CHARLIM];//The text that has been adjusted for the allowed letters
int length;

// initialisation for accelerometer
alt_8 pwm = 0;
alt_u8 led;
int level;
float filter_coeffs[N_TAPS] = {0.2, 0.2, 0.2, 0.2, 0.2};
float filter_buffer[N_TAPS] = {0}; // Buffer to store past values

alt_32 x_read;
alt_32 filtered_x_read;
alt_up_accelerometer_spi_dev * acc_dev;

// initialisation for button display
int button_data;

// function for seven segment display
//Updates the text from the console once the program is running
void updateText(){
	clearActualText();	//Clear the text from the display
	// alt_putstr("Put your new text into the console and press ENTER\n");
	prevLetter = '!';
	prevLetter = getTxt(prevLetter);
	length = getActualText();		//Adjust for special characters such as 'W' or 'M'
	if(length > 0)
		text[length-1] = '\0';		//Get rid of any extra stuff at the end
	return;
}

//Gets the text the user placed on the console
char getTxt(char curr){
	if(curr == '\n')
		return curr;
	int idx = 0;	//Keep track of what we are adding
	char newCurr = curr;
	//Keep adding characters until we get to the end of the line
	while (newCurr != '\n'){
		enteredText[idx] = newCurr;	//Add the next letter to the entered text register
		idx ++;
		newCurr = alt_getchar();	//Get the next character
	}
	length = idx;
	return newCurr;
}
//Takes the user's input and only uses the allowed letters.  Returns the length of the string entered
int getActualText(){
	int idx = 0;	//We need two indicies because the entered and actual text sequences need not be aligned
	char currentLetter; //Keeps track of the character we are wanting to add
	//Go through each letter in the entered text
	for (int i = 0; i <= length; i++){
		currentLetter = enteredText[i];
		if (currentLetter > 96){
			//Gets only the uppercase letter
			currentLetter -= 32;
		}
		switch(currentLetter){
		case 'M':
			//We build the letter "M" from two "n's," so we need to change the index twice in the actual text
			text[idx] = 'N';
			text[idx + 1] = 'N';
			idx += 2;
			break;
		case 'W':
			//We build the letter "W" from two "v's," so we need to change the index twice in the actual text
			text[idx] = 'V';
			text[idx + 1] = 'V';
			idx += 2;
			break;
		default:
			//Copy the new letter into the actual text
			text[idx] = currentLetter;
			idx++;
		}


	}
	return idx;
}
//This function clears the text on the display:
void clearActualText(){
	for(int i = 0; i <= length; i++){
		text[i] = '\0';
	}
	return;
}

//Gets the binary representation of the character
int getBin(char letter){
	/*Based on the character entered, we convert to binary so the 7-segment knows which lights to turn on.
	The 7-segment has inverted logic so a 0 means the light is on and a 1 means the light is off.
	The rightmost bit starts the index at HEX#[0], and the leftmost bit is HEX#[6], the pattern
	for the 7-segment is shown in the DE0_C5 User Manual*/
	switch(letter){
	case '0':
		return 0b1000000;
	case '1':
		return 0b1111001;
	case '2':
		return 0b0100100;
	case '3':
		return 0b0110000;
	case '4':
		return 0b0011001;
	case '5':
		return 0b0010010;
	case '6':
		return 0b0000010;
	case '7':
		return 0b1111000;
	case '8':
		return 0b0000000;
	case '9':
		return 0b0010000;
	case 'A':
		return 0b0001000;
	case 'B'://Lowercase
		return 0b0000011;
	case 'C':
		return 0b1000110;
	case 'D'://Lowercase
		return 0b0100001;
	case 'E':
		return 0b0000110;
	case 'F':
		return 0b0001110;
	case 'G':
		return 0b0010000;
	case 'H':
		return 0b0001001;
	case 'I':
		return 0b1111001;
	case 'J':
		return 0b1110001;
	case 'K':
		return 0b0001010;
	case 'L':
		return 0b1000111;
	case 'N':
		return 0b0101011;
	case 'O':
		return 0b1000000;
	case 'P':
		return 0b0001100;
	case 'Q':
		return 0b0011000;
	case 'R'://Lowercase
		return 0b0101111;
	case 'S':
		return 0b0010010;
	case 'T':
		return 0b0000111;
	case 'U':
		return 0b1000001;
	case 'V':
		return 0b1100011;
	case 'X':
		return 0b0011011;
	case 'Y':
		return 0b0010001;
	case 'Z':
		return 0b0100100;
	default:
		return 0b1111111;
	}
}

//Prints each of the letters out to the screen
void print(int let5, int let4, int let3, int let2, int let1, int let0){
	//Takes the binary value for each letter and places it on each of the six 7-segment displays
	IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, let5);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, let4);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, let3);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, let2);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX1_BASE, let1);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX0_BASE, let0);
	return;
}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x9000);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);
}

void SevenSegmentDisplay() {
    // Update the text if required (when re-enter is triggered)
    updateText();
	// alt_printf("Text: %s\n", 'about to print');
    // Display the current text on the 7-segment display
    print(getBin(text[1]), getBin(text[2]), getBin(text[3]), getBin(text[4]), getBin(text[5]), getBin(text[6]));
}

// function for accelerometer
void led_write(alt_u8 accelerometer_pattern, int button_datain) {
    //convert accelerometer pattern to int
    int acceleromter_pattern_int = (int)accelerometer_pattern;
    //OR the two patterns
    int or_pattern = acceleromter_pattern_int | button_datain;
    IOWR(LED_BASE, 0, or_pattern);
}

void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

float apply_filter(alt_32 new_reading) {
    // Shift the old samples
    for (int i = N_TAPS - 1; i > 0; i--) {
        filter_buffer[i] = filter_buffer[i - 1];
    }

    // Add the new sample
    filter_buffer[0] = (float)new_reading;

    // Apply the filter
    float filtered_value = 0;
    for (int i = 0; i < N_TAPS; i++) {
        filtered_value += filter_buffer[i] * filter_coeffs[i];
    }

    return filtered_value;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1, button_data);
        } else {
            led_write(led >> 1, button_data);
        }

    } else {
        led_write(led, button_data);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

	// Read the button
	button_data = button_display();
	// Read the accelerometer
    alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
    alt_printf("raw data: %x ", x_read);

    // Apply the filter
//    filtered_x_read = (alt_32)apply_filter(x_read);
//    alt_printf("filtered data: %x\n", filtered_x_read);
    convert_read(x_read, & level, & led);

}

// function for button display
int button_display() {
    int button_datain; // Variable to store the input from the buttons

    // Gets the data from the push button, recall that a 0 means the button is pressed
    button_datain = ~IORD_ALTERA_AVALON_PIO_DATA(BUTTON_BASE);

    // Mask the bits so the leftmost LEDs are off (we only care about LED3-0)
    button_datain &= (0b0000000011);

    // Shift the bits to correspond to the LEDs
    button_datain = button_datain << 8;
    if (button_datain == 0x100)
        alt_printf("Button Status: %s\n", "key0");
    else if (button_datain == 0x200)
        alt_printf("Button Status: %s\n", "key1");
    else{
    alt_printf("Button Status: key N/A\n");
    }

    return button_datain;
    // Send the data to the LED
    // IOWR_ALTERA_AVALON_PIO_DATA(LED_BASE, button_datain);
}


int main() {
//    alt_putstr("Hello from Nios II!\n");
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    print(getBin('!'), getBin('!'), getBin('!'), getBin('!'), getBin('!'), getBin('!'));

    if (acc_dev == NULL) {
        alt_printf("Error: could not open acc device\n");
        return 1;
    }

    timer_init(sys_timer_isr);

    while (1) {
        SevenSegmentDisplay();
    }

    return 0;
}
