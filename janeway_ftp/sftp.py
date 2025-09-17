import os
import logging
import paramiko


def ensure_remote_directory(sftp_client, remote_path):
    directories = remote_path.split('/')
    current_path = ''
    for directory in directories:
        if directory:
            current_path += f'/{directory}'
            try:
                sftp_client.stat(current_path)
            except FileNotFoundError:
                logging.info(f"Creating remote directory: {current_path}")
                sftp_client.mkdir(current_path)


def send_file_via_sftp(
        ftp_server,
        ftp_username,
        ftp_password,
        remote_file_path,
        file_path,
        file_name,
        known_hosts_file=None,
        confirm_file_sent=True,
):

    ssh = paramiko.SSHClient()
    sftp = None  # Ensure sftp is defined before usage

    if known_hosts_file:
        try:
            ssh.load_host_keys(known_hosts_file)
            logging.info(f"Loaded known hosts from {known_hosts_file}")
        except IOError as e:
            logging.warning(f"Could not load known hosts file: {e}")
    else:
        logging.warning("No known hosts file supplied. Using auto-add policy.")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            ftp_server,
            username=ftp_username,
            password=ftp_password,
        )
        sftp = ssh.open_sftp()

        # Ensure the remote directory structure exists
        ensure_remote_directory(sftp, remote_file_path)

        upload_path = f"{remote_file_path}/{file_name}"
        sftp.put(file_path, upload_path, confirm=confirm_file_sent)
        logging.info(f"File uploaded successfully to {upload_path}")
    except Exception as e:
        logging.error(f"Failed to send file via SFTP: {e}")
        raise
    finally:
        if sftp is not None:
            sftp.close()
        ssh.close()
