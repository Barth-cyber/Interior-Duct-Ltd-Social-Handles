#!/usr/bin/env python3
"""
Create a short mapping file under links/<id>.json containing the links array.
Commits the file to git and pushes to origin.
Usage: python create_short_link.py path/to/links.json
Or it will create a mapping for the default links if no arg provided.
"""
import sys, json, os, random, string, subprocess

REPO_ROOT = os.path.dirname(__file__)
LINKS_DIR = os.path.join(REPO_ROOT, 'links')

DEFAULT_LINKS = [
    { 'label': 'WhatsApp Business', 'platform': 'whatsapp', 'url': 'https://wa.me/c/2348036850229' },
    { 'label': 'Instagram', 'platform': 'instagram', 'url': 'https://www.instagram.com/interiorductltd/' },
    { 'label': 'TikTok', 'platform': 'tiktok', 'url': 'https://www.tiktok.com/@interiorductltd' },
    { 'label': 'Facebook', 'platform': 'facebook', 'url': 'https://www.facebook.com/interior.duct.ltd/' },
    { 'label': 'X (Twitter)', 'platform': 'twitter', 'url': 'https://x.com/InteriorDuctLtd' },
    { 'label': 'YouTube', 'platform': 'youtube', 'url': 'https://www.youtube.com/@InteriorDuctLtd' },
    { 'label': 'LinkedIn', 'platform': 'linkedin', 'url': 'https://www.linkedin.com/company/interior-duct-ltd/' }
]


def rand_id(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def write_mapping(links, id=None):
    if not os.path.exists(LINKS_DIR):
        os.makedirs(LINKS_DIR, exist_ok=True)
    if id is None:
        id = rand_id(6)
    path = os.path.join(LINKS_DIR, f"{id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False, indent=2)
    return id, path


def git_add_commit_push(path, message):
    try:
        subprocess.check_call(['git', 'add', path], cwd=REPO_ROOT)
        subprocess.check_call(['git', 'commit', '-m', message], cwd=REPO_ROOT)
        subprocess.check_call(['git', 'push', 'origin', 'main'], cwd=REPO_ROOT)
        return True
    except subprocess.CalledProcessError as e:
        print('Git operation failed:', e)
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = sys.argv[1]
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                links = json.load(f)
        else:
            print('File not found:', p); sys.exit(1)
    else:
        links = DEFAULT_LINKS

    new_id, new_path = write_mapping(links)
    print('Wrote mapping to', new_path)
    ok = git_add_commit_push(new_path, f'Add short-link mapping {new_id}')
    if ok:
        print('Pushed to origin. Short URL: idl.app?id=' + new_id)
    else:
        print('Failed to push mapping to remote. Short file created locally at', new_path)
