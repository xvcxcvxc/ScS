import os
import multiprocessing
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))

log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
log_file = os.path.join(script_dir, log_filename)

search_terms = [
    "k12.al.us", "k12.ak.us", "k12.az.us", "k12.ar.us", "k12.ca.us", "k12.co.us", "k12.ct.us",
    "k12.de.us", "k12.fl.us", "k12.ga.us", "k12.hi.us", "k12.id.us", "k12.il.us", "k12.in.us",
    "k12.ia.us", "k12.ks.us", "k12.ky.us", "k12.la.us", "k12.me.us", "k12.md.us", "k12.ma.us",
    "k12.mi.us", "k12.mn.us", "k12.ms.us", "k12.mo.us", "k12.mt.us", "k12.ne.us", "k12.nv.us",
    "k12.nh.us", "k12.nj.us", "k12.nm.us", "k12.ny.us", "k12.nc.us", "k12.nd.us", "k12.oh.us",
    "k12.ok.us", "k12.or.us", "k12.pa.us", "k12.ri.us", "k12.sc.us", "k12.sd.us", "k12.tn.us",
    "k12.tx.us", "k12.ut.us", "k12.vt.us", "k12.va.us", "k12.wa.us", "k12.wv.us", "k12.wi.us",
    "k12.wy.us"
]

def search_in_file(file_path, search_terms, lock, seen_matches):
    """Search for terms in a file and write matches to per-term log files."""
    file_name = os.path.basename(file_path)
    matches_by_term = {}

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                for term in search_terms:
                    if term in line:
                        match_key = f"{term}|{file_path}|{line_num}|{line.strip()}"
                        if match_key not in seen_matches:
                            result = f"[{file_name} - Line {line_num}]: {line.strip()}\n"
                            matches_by_term.setdefault(term, []).append(result)
                            seen_matches[match_key] = True
    except Exception as e:
        error = f"Error reading {file_name}: {e}\n"
        print(error)

    if matches_by_term:
        with lock:
            for term, lines in matches_by_term.items():
                log_path = os.path.join(script_dir, f"{term}.txt")
                with open(log_path, "a", encoding="utf-8") as log:
                    log.writelines(lines)
                    for line in lines:
                        print(line, end="")

def main():
    folder_path = input("Enter the folder path to search in: ").strip()

    if not os.path.isdir(folder_path):
        print(f"Invalid folder path: {folder_path}")
        return

    search_terms = [
        "k12.al.us", "k12.ak.us", "k12.az.us", "k12.ar.us", "k12.ca.us",
        "k12.co.us", "k12.ct.us", "k12.de.us", "k12.fl.us", "k12.ga.us",
        "k12.hi.us", "k12.id.us", "k12.il.us", "k12.in.us", "k12.ia.us",
        "k12.ks.us", "k12.ky.us", "k12.la.us", "k12.me.us", "k12.md.us",
        "k12.ma.us", "k12.mi.us", "k12.mn.us", "k12.ms.us", "k12.mo.us",
        "k12.mt.us", "k12.ne.us", "k12.nv.us", "k12.nh.us", "k12.nj.us",
        "k12.nm.us", "k12.ny.us", "k12.nc.us", "k12.nd.us", "k12.oh.us",
        "k12.ok.us", "k12.or.us", "k12.pa.us", "k12.ri.us", "k12.sc.us",
        "k12.sd.us", "k12.tn.us", "k12.tx.us", "k12.ut.us", "k12.vt.us",
        "k12.va.us", "k12.wa.us", "k12.wv.us", "k12.wi.us", "k12.wy.us",
    ]

    txt_files = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name.endswith(".txt"):
                file_path = os.path.join(root, name)
                try:
                    mtime = os.path.getmtime(file_path)
                    txt_files.append((file_path, mtime))
                except Exception as e:
                    print(f"Could not access {file_path}: {e}")

    if not txt_files:
        print("No text files found in the directory.")
        return

    txt_files.sort(key=lambda x: x[1], reverse=True)
    sorted_file_paths = [file[0] for file in txt_files]

    multiprocessing.freeze_support()
    with multiprocessing.Manager() as manager:
        lock = manager.Lock()
        seen_matches = manager.dict()
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.starmap(
                search_in_file,
                [(file, search_terms, lock, seen_matches) for file in sorted_file_paths]
            )

if __name__ == "__main__":
    main()
