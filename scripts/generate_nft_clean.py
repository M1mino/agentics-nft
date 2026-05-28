#!/usr/bin/env python3
"""Generate 1000 NFT images — clean: agent icon only, no frames, no text."""

import json, os
from PIL import Image

ICON_DIR = "images"
OUT_DIR = "images/nft"
MAPPING_FILE = "scripts/nft_mapping.json"

def get_agent_icon(agent_name):
    fname = agent_name.lower().replace(" ", "-") + ".png"
    path = os.path.join(ICON_DIR, fname)
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    return None

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    with open(MAPPING_FILE) as f:
        mapping = json.load(f)
    
    total = len(mapping)
    nft_ids = sorted(mapping.keys(), key=int)
    
    print(f"🎨 Generating {total} clean NFT images...")
    print(f"   Output: {OUT_DIR}/\n")
    
    success = 0
    for i, nft_id in enumerate(nft_ids):
        agent_name = mapping[nft_id]
        icon = get_agent_icon(agent_name)
        if icon is None:
            print(f"  ⚠️ No icon for {agent_name}, #{nft_id}")
            continue
        
        # Just save the raw icon as-is
        out_path = os.path.join(OUT_DIR, f"{nft_id}.png")
        icon.save(out_path, "PNG")
        success += 1
        
        if (i+1) % 200 == 0:
            print(f"  ✅ {i+1}/{total}")
    
    print(f"\n✅ Done: {success}/{total} clean images")

if __name__ == "__main__":
    main()
