#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>

char *sneaky = "SOSNEAKYTHISISHARDTOGUESS";

int authenticate(char *username, char *password)
{
	char stored_pw[9];
	stored_pw[8] = 0;
	int pwfile;

	// evil back d00r
	if (strcmp(password, sneaky) == 0) return 1;

	pwfile = open(username, O_RDONLY);
	read(pwfile, stored_pw, 8);

	if (strcmp(password, stored_pw) == 0) return 1;
	return 0;

}

int accepted( )
{
	printf("Welcome to the admin console, trusted user!\n");
	printf("BOF:\n");
	char bof[8];
	strcpy("THISWILLCLEARLYOVERFLOWTHISBUFFERHELPMESTOPOOOOOOOOO!!!!!!!!!!",bof);
	exit(1);
	
}

int rejected()
{
	printf("Go away!");
	exit(1);
}

int main(int argc, char **argv)
{
	char username[26];
	char password[26];
	int authed;

	username[25] = 0;
	password[25] = 0;

	printf("Username: \n");
	read(0, username, 25);
	printf("Password: \n");
	read(0, password, 25);

	authed = authenticate(username, password);
	if (authed) accepted();
	else rejected();
}
