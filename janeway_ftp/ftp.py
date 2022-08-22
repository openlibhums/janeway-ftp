import os

from ftplib import FTP, error_perm


def send_file_via_ftp(
    ftp_server,
    ftp_username,
    ftp_password,
    file_path,
    remote_directory='janeway',
):

    file_to_send = open(file_path, 'rb')
    file_name = os.path.basename(file_to_send.name)

    ftp_client = FTP(ftp_server)
    ftp_client.login(
        user=ftp_username,
        passwd=ftp_password,
    )
    try:
        ftp_client.mkd(remote_directory)
    except error_perm:
        # janeway dir exists, skip
        pass

    ftp_client.cwd(remote_directory)

    ftp_client.storbinary(
        'STOR {file_name}'.format(file_name=file_name),
        file_to_send
    )

    # Close file, FTP Session and unlink the zip file
    file_to_send.close()
    ftp_client.quit()
