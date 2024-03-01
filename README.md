# URL Generator

## Overview

`generate_valid_invalid_urls.py` is a Python script for generating valid URLs by assembling URL components such as scheme, authority, path, query, and fragment, in accordance with RFC 3986 standards. It also includes a method for generating invalid URLs.

## Features

### Character Generation
- Functions are designed to generate different types of characters needed for URLs, including percent-encoded characters, general delimiters, sub-delimiters, reserved, and unreserved characters.

### Scheme Generation
- Random URL schemes are generated, which are crucial for defining the protocol to be used.

### Authority Component
- Constructs the authority part, including user information, host (IPv4, IPv6, future IP versions), and port, essential for locating the resource.

### Path Component
- Generates paths in various forms, pivotal for specifying the resource location on the server.

### Query and Fragment
- Supports the creation of query and fragment components, used for providing additional data and navigating within a page.

## Function Explanations Based on RFC 3986

- **Percent-encoding**: Essential for encoding characters that may not be safely sent in URLs.
- **Scheme**: Defines the protocol used for the URL, such as HTTP or HTTPS.
- **Authority**: Specifies the domain name or IP address and port number, indicating the server.
- **Path**: Identifies the specific resource within the server.
- **Query**: Provides additional information to the server for resource retrieval.
- **Fragment**: Allows direct access to a subsection of the resource.

## Usage

1. **Installation**: No external dependencies required.
2. **Execution**: `python generate_valid_invalid_urls.py`
3. **Output**: Prints 100 valid URLs to the console.

## Customization

- Adjust the `N` variable to change the number of URLs generated.
- Modify maximum lengths for different components in their respective functions.

## Contribution

Contributions are welcome for improvements or new features.

## License

Open-sourced under the MIT License.
