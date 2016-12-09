#include "main.h"

int main() {

	void(*FACE_IO_Initialize_TEST_PTR) (
		/* in     */ FACE_CONFIGURATION_RESOURCE configuration,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Initialize;

	void(*FACE_IO_Open_TEST_PTR) (
		/* in     */ FACE_INTERFACE_NAME_TYPE name,
		/* in     */ FACE_TIMEOUT_TYPE timeout,
		/*    out */ FACE_INTERFACE_HANDLE_TYPE *handle,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Open;

	void(*FACE_IO_Register_TEST_PTR) (
		/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
		/* in     */ FACE_CALLBACK_ADDRESS_TYPE callback_address,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Register;
	
	/* Function Signature Conformance Test */
	void(*FACE_IO_Unregister_TEST_PTR) (
		/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Unregister;


	/* Function Signature Conformance Test */
	void(*FACE_IO_Read_TEST_PTR) (
		/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
		/* in     */ FACE_TIMEOUT_TYPE timeout,
		/* in out */ FACE_MESSAGE_LENGTH_TYPE *message_length,
		/* in     */ FACE_MESSAGE_ADDR_TYPE data_buffer_address,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Read;


	/* Function Signature Conformance Test */
	void(*FACE_IO_Write_TEST_PTR) (
		/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
		/* in     */ FACE_TIMEOUT_TYPE timeout,
		/* in     */ FACE_MESSAGE_LENGTH_TYPE message_length,
		/* in     */ FACE_MESSAGE_ADDR_TYPE data_buffer_address,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Write;


	/* Function Signature Conformance Test */
	void(*FACE_IO_Get_Status_TEST_PTR) (
		/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
		/*    out */ FACE_STATUS_TYPE *status,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Get_Status;


	/* Function Signature Conformance Test */
	void(*FACE_IO_Close_TEST_PTR) (
		/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
		/*    out */ FACE_RETURN_CODE_TYPE *return_code
		) = FACE_IO_Close;

	
	return 0;
}