import os
import sys


root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)


try:
    import pygit2
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    branch_name = repo.head.shorthand

    remote_name = 'origin'
    remote = repo.remotes[remote_name]

    remote.fetch()

    local_branch_ref = f'refs/heads/{branch_name}'
    local_branch = repo.lookup_reference(local_branch_ref)

    remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
    remote_commit = repo.revparse_single(remote_reference)

    merge_result, _ = repo.merge_analysis(remote_commit.id)

    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print("Already up-to-date")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        local_branch.set_target(remote_commit.id)
        repo.head.set_target(remote_commit.id)
        repo.checkout_tree(repo.get(remote_commit.id))
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
        print("Fast-forward merge")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print("Update failed - Did you modify any file?")
except Exception as e:
    print('Update failed.')
    print(str(e))

print('Update succeeded.')

########

from pathlib import Path

# Change directory to /tmp/
os.chdir("/tmp/")

# Create directory All_Models if it doesn't exist
models_dir = "/tmp/All_Models"
os.makedirs(models_dir, exist_ok=True)

# Change directory to /tmp/All_Models
os.chdir(models_dir)

# Create necessary subdirectories
subdirectories = ['checkpoints', 'loras', 'embeddings', 'vae_approx', 'upscale_models', 'inpaint', 'clip_vision', 'controlnet']
for subdir in subdirectories:
    os.makedirs(subdir, exist_ok=True)

# Store models_dir
with open("models_dir.txt", "w") as f:
    f.write(models_dir)

# Remove existing directories in /notebooks/Fooocus/models
existing_dirs = ['checkpoints', 'loras', 'embeddings', 'vae_approx', 'upscale_models', 'inpaint', 'clip_vision', 'controlnet']
for subdir in existing_dirs:
    os.system(f"rm -rf /notebooks/Fooocus/models/{subdir}")

# Create symlinks
symlinks = [
    (Path(models_dir) / "checkpoints", Path('/notebooks/Fooocus/models/checkpoints')),
    (Path(models_dir) / "loras", Path('/notebooks/Fooocus/models/loras')),
    (Path(models_dir) / "embeddings", Path('/notebooks/Fooocus/models/embeddings')),
    (Path(models_dir) / "vae_approx", Path('/notebooks/Fooocus/models/vae_approx')),
    (Path(models_dir) / "upscale_models", Path('/notebooks/Fooocus/models/upscale_models')),
    (Path(models_dir) / "inpaint", Path('/notebooks/Fooocus/models/inpaint')),
    (Path(models_dir) / "controlnet", Path('/notebooks/Fooocus/models/clip_vision')),
    (Path(models_dir) / "controlnet", Path('/notebooks/Fooocus/models/controlnet')),
]

for src, dest in symlinks:
    if dest.is_symlink() and not dest.exists(): 
        print('Symlink broken, removing:', dest)
        dest.unlink()
    if not dest.exists():
        os.symlink(src, dest)
    print(os.path.realpath(dest), '->', dest)

print('Symlinks created.')

os.chdir(root)


########


#from launch import *
