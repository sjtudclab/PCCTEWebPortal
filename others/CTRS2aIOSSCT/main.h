typedef int FACE_CONFIGURATION_RESOURCE;
typedef int FACE_RETURN_CODE_TYPE;
typedef int FACE_INTERFACE_NAME_TYPE;
typedef int FACE_TIMEOUT_TYPE;
typedef int FACE_INTERFACE_HANDLE_TYPE;
typedef int FACE_RETURN_CODE_TYPE;
typedef int FACE_INTERFACE_HANDLE_TYPE;
typedef int FACE_CALLBACK_ADDRESS_TYPE;
typedef int FACE_RETURN_CODE_TYPE;
typedef int FACE_INTERFACE_HANDLE_TYPE;
typedef int FACE_RETURN_CODE_TYPE;
typedef int FACE_INTERFACE_HANDLE_TYPE;
typedef int FACE_TIMEOUT_TYPE;
typedef int FACE_MESSAGE_LENGTH_TYPE;
typedef int FACE_MESSAGE_ADDR_TYPE;
typedef int FACE_RETURN_CODE_TYPE;
typedef int FACE_INTERFACE_HANDLE_TYPE;
typedef int FACE_TIMEOUT_TYPE;
typedef int FACE_MESSAGE_LENGTH_TYPE;
typedef int FACE_MESSAGE_ADDR_TYPE;
typedef int FACE_RETURN_CODE_TYPE;
typedef int FACE_INTERFACE_HANDLE_TYPE;
typedef int FACE_STATUS_TYPE;
typedef int FACE_RETURN_CODE_TYPE;
typedef int FACE_INTERFACE_HANDLE_TYPE;
typedef int FACE_RETURN_CODE_TYPE;


void FACE_IO_Initialize(
	/* in     */ FACE_CONFIGURATION_RESOURCE configuration,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);

void FACE_IO_Open(
	/* in     */ FACE_INTERFACE_NAME_TYPE name,
	/* in     */ FACE_TIMEOUT_TYPE timeout,
	/*    out */ FACE_INTERFACE_HANDLE_TYPE *handle,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);

void FACE_IO_Register(
	/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
	/* in     */ FACE_CALLBACK_ADDRESS_TYPE callback_address,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);

void FACE_IO_Unregister(
	/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);

void FACE_IO_Read(
	/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
	/* in     */ FACE_TIMEOUT_TYPE timeout,
	/* in out */ FACE_MESSAGE_LENGTH_TYPE *message_length,
	/* in     */ FACE_MESSAGE_ADDR_TYPE data_buffer_address,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);

void FACE_IO_Write(
	/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
	/* in     */ FACE_TIMEOUT_TYPE timeout,
	/* in     */ FACE_MESSAGE_LENGTH_TYPE message_length,
	/* in     */ FACE_MESSAGE_ADDR_TYPE data_buffer_address,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);

void FACE_IO_Get_Status(
	/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
	/*    out */ FACE_STATUS_TYPE *status,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);

void FACE_IO_Close(
	/* in     */ FACE_INTERFACE_HANDLE_TYPE handle,
	/*    out */ FACE_RETURN_CODE_TYPE *return_code
	);
