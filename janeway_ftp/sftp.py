import os
import logging
import paramiko


def send_file_via_sftp(
        ftp_server,
        ftp_username,
        ftp_password,
        ftp_server_key,
        remote_file_path,
        file_path,
        file_name
):
    ssh = paramiko.SSHClient()
    if ftp_server_key:
        key = paramiko.ecdsakey.ECDSAKey(
            data=paramiko.py3compat.decodebytes(ftp_server_key.encode("utf8"))
        )
        ssh.get_host_keys().add(
            hostname=ftp_server,
            keytype="ecdsa",
            key=key,
        )
    else:
        logging.warning("No PORTICO_FTP_SERVER_KEY configured")
        ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())

    ssh.connect(
        ftp_server,
        username=ftp_username,
        password=ftp_password,
    )
    sftp = ssh.open_sftp()
    try:
        sftp.mkdir(
            remote_file_path,
        )
    except IOError:
        pass # folder exists already
    upload_path = "{}/{}".format(remote_file_path, file_name)
    sftp.put(
        file_path,
        upload_path,
    )

    # Close SFTP Session and unlink the zip file
    ssh.close()

