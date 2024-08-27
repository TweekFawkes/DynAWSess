# DynAWSess

DynAWSess (pronounced "Dine-Access") is a Python script that automates the process of updating AWS EC2 security groups with your current IP address for specific ports (22, 81, and 5000).

## About the Name

The name "DynAWSess" is a portmanteau of three key aspects of the application:

- **Dyn**: Short for "Dynamic", representing the script's ability to adapt to changing IP addresses.
- **AWS**: Stands for Amazon Web Services, the cloud platform this script interacts with.
- **ess**: Derived from "Access", highlighting the script's role in managing access control.

Pronounced as "Dine-Access", the name encapsulates the idea of "dining" or consuming AWS access dynamically.

## Features

- Retrieves your current public IP address
- Loads AWS credentials from a config file
- Updates EC2 security groups in the specified AWS region
- Displays cool ASCII art using pyfiglet

## Prerequisites

- Python 3.7+
- AWS account with appropriate permissions
- AWS Access Key ID and Secret Access Key

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/dynawsess.git
   cd dynawsess
   ```

2. Create a virtual environment and activate it:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a `dynawsess.config` file in the same directory as the script:

   ```
   AWS_REGION=us-west-2
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   ```

   Replace `your_access_key_id` and `your_secret_access_key` with your actual AWS credentials.

## Usage

Run the script:

```
python dynawsess.py
```

The script will display ASCII art, fetch your current IP address, and update the specified security group rules for all EC2 instances in the configured AWS region.

## Security Considerations

- Keep your AWS credentials secure and never commit them to version control.
- Use IAM roles and policies to limit the permissions of the AWS user associated with these credentials.
- Consider using AWS Secrets Manager or similar services for more secure credential management in production environments.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
