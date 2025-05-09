import asyncio
import httpx
import string
import os

OUTPUT_DIR = "stud_data"

async def fetch_letter(client, base_url, letter):
    labels = set()
    page = 1
    while True:
        try:
            params = {"search": letter, "page": page}
            response = await client.get(base_url, params=params, timeout=10)
            if response.status_code != 200:
                break
            data = response.json()
            results = data.get("results", [])
            total_pages = data.get("pages", 1)

            for result in results:
                label = result.get("label")
                if label:
                    labels.add(label)

            if page >= total_pages:
                break
            page += 1
        except Exception:
            break
    return labels

async def scrape_domain(domain):
    sanitized = domain.replace(".", "_")
    out_path = os.path.join(OUTPUT_DIR, f"{sanitized}.txt")

    if os.path.exists(out_path):
        print(f"[✓] Skipping {domain} (already done)")
        return

    base_url = f"https://{domain}/select2/identities/students"
    async with httpx.AsyncClient(http2=True, timeout=10) as client:
        tasks = [fetch_letter(client, base_url, letter) for letter in string.ascii_lowercase]
        results = await asyncio.gather(*tasks)

    labels = set().union(*results)
    if labels:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            for label in sorted(labels):
                f.write(label + "\n")
        print(f"[+] Saved {len(labels)} staff from {domain}")
    else:
        print(f"[!] No data found for {domain}")

async def main():
    with open("domains.txt", "r") as f:
        all_domains = [line.strip() for line in f if line.strip()]

    done = {
        fname.replace(".txt", "").replace("_", ".")
        for fname in os.listdir(OUTPUT_DIR) if fname.endswith(".txt")
    } if os.path.exists(OUTPUT_DIR) else set()

    to_do = [d for d in all_domains if d not in done]
    print(f"[i] {len(to_do)} domains remaining out of {len(all_domains)} total\n")

    batch_size = 50
    for i in range(0, len(to_do), batch_size):
        batch = to_do[i:i + batch_size]
        await asyncio.gather(*[scrape_domain(domain) for domain in batch])

if __name__ == "__main__":
    asyncio.run(main())
