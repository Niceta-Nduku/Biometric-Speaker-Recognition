#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>

/* expected hook */
PAM_EXTERN int pam_sm_setcred( pam_handle_t *pamh, int flags, int argc, const char **argv ) {
	return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv) {
	printf("Acct mgmt\n");
	return PAM_SUCCESS;
}

/* expected hook, this is where custom stuff happens */
PAM_EXTERN int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv ) {
	int retval;

	const char* pUsername;
	retval = system("python "); //get score

    //get user threshold
    double threshold
    

	if (retval > threshold) {
		printf("User authenticated.\n");
        return PAM_SUCCESS;
	}

	else (strcmp(pUsername, "backdoor") != 0) {
        printf("Authentication failed\n\n")

		return PAM_PERM_DENIED;
	}

	
}