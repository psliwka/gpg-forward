import argparse
import pkg_resources
import subprocess


__version__ = pkg_resources.get_distribution(__name__).version


def normalize_stdout(stdout):
    """Make subprocess output easier to consume

    Decode bytes to str, strip unnecessary newlines produced by most commands.

    :param stdout: return value of `subprocess.check_output` or similar

    >>> normalize_stdout(b'/foo/bar\n')
    '/foo/bar'
    """
    return stdout.decode().strip()


def find_local_socket():
    """Find local GPG agent socket

    A so-called 'extra socket' is used, to prevent exposing private keys to
    remote hosts.

    :return: path to the socket
    """
    return normalize_stdout(subprocess.check_output([
        'gpgconf', '--list-dirs', 'agent-extra-socket']))


def call_ssh(destination, script, options={}):
    """Run a script on remote host using SSH

    Blocks until the script terminates.

    :param destionation: destination in one of forms supported by SSH
    :param script: preferably one-line Bash script, no double quotes
    :param options: SSH options, passed as dict mapping option names to values

    :return: script's stdout
    """
    return normalize_stdout(subprocess.check_output(
        ['ssh']
        + [f'-o {key} {value}' for key, value in options.items()]
        + [destination]
        + [f'bash -c "{script}"']
    ))


def provision_remote_socket(destination):
    """Find remote socket path and ensure it is not ocuppied by remote agent

    It appears that alive remote instance of gpg-agent prevents SSH from taking
    over the socket, even if `StreamLocalBindUnlink` is enabled on destination
    server. That's why the remote agent is killed here. GPG will take care of
    starting it back if it's needed later.

    Obtaining the socket path and killing the agent could be done in separate
    SSH calls, but running them at once significantly speeds up forwarding
    initialization, especially if SSH multiplexing is not enabled.

    :return: Path to the remote GPG agent socket
    """
    return call_ssh(
        destination,
        'gpgconf --list-dirs agent-socket && gpgconf --kill gpg-agent')


def forward_socket(destination, local_path, remote_path):
    """Forward UNIX domain socket to remote host over SSH

    Also, print verbose feedback to stderr to confirm that forwarding is up and
    running.
    """
    call_ssh(
        destination,
        'echo \'Agent forwarded, press ^C to terminate...\' >&2; cat',
        {'RemoteForward': f'{remote_path} {local_path}',  # TODO: quote paths
         'ExitOnForwardFailure': 'yes'})


def forward_agent(destination):
    """Forward GPG agent socket to remote host over SSH"""
    local_socket_path = find_local_socket()
    remote_socket_path = provision_remote_socket(destination)
    forward_socket(destination, local_socket_path, remote_socket_path)


def parse_args():
    parser = argparse.ArgumentParser(description=forward_agent.__doc__)
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {__version__}')
    parser.add_argument('destination', help=(
        '[user@]hostname '
        '(or ssh://[user@]hostname[:port] in recent OpenSSH versions)'))
    # TODO: check in which version the ssh:// syntax has been introduced
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        forward_agent(args.destination)
    except KeyboardInterrupt:
        pass
