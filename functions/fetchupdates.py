from git import Repo, GitCommandError

def check_for_updates():
    repo = Repo("https://github.com/Shreyas-ITB/VerusStatisticsAPI")
    try:
        repo.remotes.origin.fetch()
        local_commit = repo.head.commit.hexsha
        remote_commit = repo.remotes.origin.refs.main.commit.hexsha
        if local_commit != remote_commit:
            short_commit = remote_commit[:7]
            print(f"New API update is available ({short_commit}), please update to the latest version!")
    except GitCommandError as e:
        print(f"An error occurred while checking for updates: {e}")