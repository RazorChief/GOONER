"""
DSS Katalog Rekomendasi Game
Berdasarkan Genre & Harga
Menggunakan: BFS Graph Traversal + Dijkstra + SAW (Simple Additive Weighting)
"""

from collections import defaultdict, deque
import heapq


# ============================================================
# DATABASE GAME — Node sesuai laporan (G1-G20)
# Harga "Free" = 0
# ============================================================
DATABASE_GAME = [
    {"id": "G1",  "nama": "Minecraft",               "genre": [
        "Sandbox"],    "harga": 538000, "rating": 9.0, "popularitas": 98},
    {"id": "G2",  "nama": "Terraria",                 "genre": [
        "Sandbox"],    "harga": 90000,  "rating": 9.2, "popularitas": 91},
    {"id": "G3",  "nama": "Stardew Valley",           "genre": [
        "Simulation"], "harga": 115000, "rating": 9.0, "popularitas": 88},
    {"id": "G4",  "nama": "Hollow Knight",            "genre": [
        "Action"],     "harga": 130000, "rating": 9.1, "popularitas": 85},
    {"id": "G5",  "nama": "Hades II",                 "genre": [
        "Action"],     "harga": 245000, "rating": 9.4, "popularitas": 90},
    {"id": "G6",  "nama": "Valorant",                 "genre": [
        "Shooter"],    "harga": 0,      "rating": 8.5, "popularitas": 95},
    {"id": "G7",  "nama": "Tekken",                   "genre": [
        "Fighting"],   "harga": 799000, "rating": 8.8, "popularitas": 82},
    {"id": "G8",  "nama": "Dragon Ball Xenoverse",    "genre": [
        "Fighting"],   "harga": 450000, "rating": 8.3, "popularitas": 78},
    {"id": "G9",  "nama": "Satisfactory",             "genre": [
        "Sandbox"],    "harga": 210000, "rating": 8.9, "popularitas": 84},
    {"id": "G10", "nama": "Zomboid",                  "genre": [
        "Shooter"],    "harga": 139000, "rating": 8.7, "popularitas": 80},
    {"id": "G11", "nama": "Fishing Simulator",        "genre": [
        "Simulation"], "harga": 0,      "rating": 7.5, "popularitas": 65},
    {"id": "G12", "nama": "7 Days to Die",            "genre": [
        "Sandbox"],    "harga": 338000, "rating": 8.2, "popularitas": 76},
    {"id": "G13", "nama": "Wuthering Wave",           "genre": [
        "RPG"],        "harga": 0,      "rating": 8.6, "popularitas": 87},
    {"id": "G14", "nama": "Blue Archive",             "genre": [
        "RPG"],        "harga": 0,      "rating": 8.4, "popularitas": 83},
    {"id": "G15", "nama": "Marvel Rivals",            "genre": [
        "Action"],     "harga": 0,      "rating": 8.5, "popularitas": 89},
    {"id": "G16", "nama": "House Flipper",            "genre": [
        "Simulation"], "harga": 206000, "rating": 8.3, "popularitas": 72},
    {"id": "G17", "nama": "Subnautica",               "genre": [
        "Sandbox"],    "harga": 350000, "rating": 9.1, "popularitas": 88},
    {"id": "G18", "nama": "Devil May Cry 5",          "genre": [
        "Action"],     "harga": 389000, "rating": 9.0, "popularitas": 86},
    {"id": "G19", "nama": "Limbus Company",           "genre": [
        "RPG"],        "harga": 0,      "rating": 8.7, "popularitas": 81},
    {"id": "G20", "nama": "Umamusume: Pretty Derby",  "genre": [
        "Simulation"], "harga": 0,      "rating": 8.2, "popularitas": 75},
]

# ============================================================
# EDGE sesuai laporan:
#   - Genre sama  -> bobot 0.1 (sangat mirip)
#   - Harga mirip -> bobot 0.3 (cukup mirip)
# Edge bersifat undirected (dua arah)
# ============================================================
EDGES_LAPORAN = [
    ("G1",  "G2",  "Genre sama",  0.1),
    ("G2",  "G3",  "Harga mirip", 0.3),
    ("G3",  "G4",  "Harga mirip", 0.3),
    ("G4",  "G5",  "Genre sama",  0.1),
    ("G5",  "G6",  "Harga mirip", 0.5),
    ("G6",  "G10", "Genre sama",  0.1),
    ("G7",  "G8",  "Genre sama",  0.1),
    ("G8",  "G9",  "Harga mirip", 0.3),
    ("G9",  "G12", "Genre sama",  0.1),
    ("G1",  "G9",  "Genre sama",  0.1),
    ("G1",  "G12", "Genre sama",  0.1),
    ("G1",  "G17", "Genre sama",  0.1),
    ("G2",  "G9",  "Genre sama",  0.1),
    ("G2",  "G12", "Genre sama",  0.1),
    ("G2",  "G17", "Genre sama",  0.1),
    ("G9",  "G17", "Genre sama",  0.1),
    ("G12", "G17", "Genre sama",  0.1),
    ("G3",  "G11", "Genre sama",  0.1),
    ("G3",  "G16", "Genre sama",  0.1),
    ("G3",  "G20", "Genre sama",  0.1),
    ("G11", "G16", "Genre sama",  0.1),
    ("G11", "G20", "Genre sama",  0.1),
    ("G16", "G20", "Genre sama",  0.1),
    ("G13", "G14", "Genre sama",  0.1),
    ("G13", "G19", "Genre sama",  0.1),
    ("G14", "G19", "Genre sama",  0.1),
    ("G4",  "G15", "Genre sama",  0.1),
    ("G4",  "G18", "Genre sama",  0.1),
    ("G5",  "G15", "Genre sama",  0.1),
    ("G5",  "G18", "Genre sama",  0.1),
    ("G15", "G18", "Genre sama",  0.1),
    ("G3",  "G20", "Harga mirip", 0.3),
]

SEMUA_GENRE = sorted(set(g for game in DATABASE_GAME for g in game["genre"]))

# Bobot SAW otomatis — tidak perlu input user
BOBOT_SAW = {
    "rating":      0.30,
    "harga":       0.20,
    "popularitas": 0.25,
    "kemiripan":   0.25,
}


# ============================================================
# STEP 1: BANGUN GRAPH GENRE
# ============================================================
def bangun_graph_genre(database):
    """
    graph    : genre -> [game_id, ...]
    adjacency: genre -> {genre tetangga} (dari EDGES_LAPORAN)
    """
    graph = defaultdict(list)
    adjacency = defaultdict(set)
    id_to_game = {g["id"]: g for g in database}

    for game in database:
        for genre in game["genre"]:
            graph[genre].append(game["id"])

    for (u, v, _, __) in EDGES_LAPORAN:
        gu = id_to_game[u]["genre"][0]
        gv = id_to_game[v]["genre"][0]
        adjacency[gu].add(gv)
        adjacency[gv].add(gu)

    return graph, adjacency


# ============================================================
# STEP 2: BFS — Cari Kandidat Game Berdasarkan Genre
# ============================================================
def bfs_cari_kandidat(start_genre, graph_genre, adjacency, kedalaman=2):
    visited = set()
    queue = deque([(start_genre, 0)])
    kandidat_ids = set()

    while queue:
        genre, depth = queue.popleft()
        if genre in visited or depth > kedalaman:
            continue
        visited.add(genre)

        for gid in graph_genre.get(genre, []):
            kandidat_ids.add(gid)

        if depth < kedalaman:
            for tetangga in adjacency.get(genre, []):
                if tetangga not in visited:
                    queue.append((tetangga, depth + 1))

    return kandidat_ids


# ============================================================
# STEP 3: BANGUN GRAPH KEMIRIPAN ANTAR GAME
# ============================================================
def hitung_kemiripan_genre(game_a, game_b):
    """Jaccard distance: 0 = identik, 1 = tidak mirip."""
    set_a = set(game_a["genre"])
    set_b = set(game_b["genre"])
    union = len(set_a | set_b)
    if union == 0:
        return 1.0
    return round(1.0 - len(set_a & set_b) / union, 4)


def bangun_graph_kemiripan(kandidat_ids, database):
    """
    Weighted graph: bobot dari EDGES_LAPORAN jika ada,
    fallback Jaccard untuk pasangan yang tidak terdaftar.
    """
    id_to_game = {g["id"]: g for g in database}
    graph = defaultdict(list)

    # Indeks cepat edge laporan (undirected)
    edge_index = {}
    for (u, v, _, bobot) in EDGES_LAPORAN:
        edge_index[(u, v)] = bobot
        edge_index[(v, u)] = bobot

    ids = list(kandidat_ids)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            bobot = edge_index.get((a, b),
                                   hitung_kemiripan_genre(id_to_game[a], id_to_game[b]))
            graph[a].append((bobot, b))
            graph[b].append((bobot, a))

    return graph, id_to_game


# ============================================================
# STEP 4: DIJKSTRA — Hitung Jarak Kemiripan
# ============================================================
def dijkstra(graph, start_id, kandidat_ids):
    dist = {gid: float('inf') for gid in kandidat_ids}
    dist[start_id] = 0
    pq = [(0, start_id)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for (w, v) in graph.get(u, []):
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return dist


# ============================================================
# STEP 5: SAW — Simple Additive Weighting
# ============================================================
def normalisasi_benefit(nilai_list):
    max_val = max(nilai_list) or 1
    return [v / max_val for v in nilai_list]


def normalisasi_cost(nilai_list):
    min_val = min((v for v in nilai_list if v > 0), default=1)
    return [min_val / v if v > 0 else 1.0 for v in nilai_list]


def hitung_saw(games, dist_kemiripan):
    if not games:
        return []

    ratings = [g["rating"] for g in games]
    harga = [g["harga"] for g in games]
    popularitas = [g["popularitas"] for g in games]
    kemiripan = [dist_kemiripan.get(g["id"], float('inf')) for g in games]

    # Ganti inf dengan nilai terburuk + 1 agar normalisasi tidak error
    max_k = max((k for k in kemiripan if k != float('inf')), default=1) + 1
    kemiripan = [k if k != float('inf') else max_k for k in kemiripan]

    norm_rating = normalisasi_benefit(ratings)
    norm_harga = normalisasi_cost(harga)
    norm_popularitas = normalisasi_benefit(popularitas)
    norm_kemiripan = normalisasi_cost(kemiripan)

    hasil = []
    for i, game in enumerate(games):
        skor = (
            BOBOT_SAW["rating"] * norm_rating[i] +
            BOBOT_SAW["harga"] * norm_harga[i] +
            BOBOT_SAW["popularitas"] * norm_popularitas[i] +
            BOBOT_SAW["kemiripan"] * norm_kemiripan[i]
        )
        hasil.append({**game, "skor_saw": round(skor, 4)})

    hasil.sort(key=lambda x: x["skor_saw"], reverse=True)
    for rank, item in enumerate(hasil, 1):
        item["rank"] = rank

    return hasil


# ============================================================
# FILTER
# ============================================================
def terapkan_filter(database, genre_filter, harga_min, harga_maks):
    """
    Logika harga:
      harga_min = 0        -> tidak ada batas bawah (Free lolos)
      harga_min > 0        -> harga harus >= harga_min (Free tidak lolos)
      harga_maks = inf     -> tidak ada batas atas
      harga_maks = nilai   -> harga harus <= harga_maks
    Logika genre:
      genre_filter = None  -> semua genre lolos
    """
    hasil = []
    for g in database:
        h = g["harga"]
        if h < harga_min:
            continue
        if harga_maks != float('inf') and h > harga_maks:
            continue
        if genre_filter is not None:
            if not any(gn in genre_filter for gn in g["genre"]):
                continue
        hasil.append(g)
    return hasil


# ============================================================
# HELPER TAMPILAN
# ============================================================
def fmt_harga(h):
    return "Free" if h == 0 else f"Rp {h:,}"


def tampilkan_header():
    print("\n" + "="*60)
    print("  🎮  DSS KATALOG REKOMENDASI GAME  🎮")
    print("       Genre & Harga — BFS + Dijkstra + SAW")
    print("="*60)


def tampilkan_katalog(database):
    print("\n📋  KATALOG GAME")
    print("-"*72)
    print(f"{'ID':<5} {'Nama Game':<30} {'Genre':<12} {'Harga':>14} {'Rating':>7}")
    print("-"*72)
    for g in database:
        print(
            f"{g['id']:<5} {g['nama']:<30} {g['genre'][0]:<12} {fmt_harga(g['harga']):>14} {g['rating']:>7.1f}")
    print("-"*72)
    print(f"  Total: {len(database)} game")


def tampilkan_rekomendasi(hasil, top_n=5):
    n = min(top_n, len(hasil))
    print(f"\n🏆  TOP {n} REKOMENDASI GAME TERBAIK")
    print(f"     Bobot SAW: Rating={BOBOT_SAW['rating']} | "
          f"Harga={BOBOT_SAW['harga']} | "
          f"Popularitas={BOBOT_SAW['popularitas']} | "
          f"Kemiripan={BOBOT_SAW['kemiripan']}")
    print("="*78)
    print(f"{'Rank':<5} {'ID':<5} {'Nama Game':<28} {'Genre':<12} {'Harga':>14} {'Skor SAW':>9}")
    print("-"*78)
    for item in hasil[:n]:
        print(f"  {item['rank']:<4} {item['id']:<5} {item['nama']:<28} "
              f"{item['genre'][0]:<12} {fmt_harga(item['harga']):>14}  {item['skor_saw']:>8.4f}")
    print("="*78)


# ============================================================
# INPUT PREFERENSI (genre + harga, dipakai di semua menu)
# ============================================================
def input_preferensi():
    """
    Input terpadu genre dan harga dalam satu fungsi, dua prompt terpisah.
    Genre 0 = All (semua genre) berlaku di semua konteks.
    Mengembalikan (genre_filter, harga_min, harga_maks)
      genre_filter = None berarti semua genre
    """
    print("\n🔍  PENGATURAN PREFERENSI")
    print("-"*50)

    # ── INPUT GENRE ──────────────────────────────────────────
    print("  Genre yang tersedia:")
    print("  0. All (semua genre)")
    for i, g in enumerate(SEMUA_GENRE, 1):
        print(f"  {i}. {g}")
    print(f"  Pilih genre (0 = semua, pisah koma untuk beberapa, contoh: 1,3)")

    while True:
        try:
            genre_raw = input("  Genre  : ").strip()
            if genre_raw == "0":
                genre_hasil = None
            else:
                indices = [int(x.strip()) - 1 for x in genre_raw.split(",")]
                genre_hasil = [SEMUA_GENRE[i]
                               for i in indices if 0 <= i < len(SEMUA_GENRE)]
                if not genre_hasil:
                    print("  ❌ Genre tidak valid, coba lagi.")
                    continue
            break
        except (ValueError, IndexError):
            print("  ❌ Input tidak valid, masukkan angka sesuai daftar.")

    # ── INPUT HARGA MIN & MAKS ────────────────────────────────
    print()
    print("  Harga dalam Rupiah. Masukkan 0 = tidak ada batas.")

    while True:
        try:
            harga_min = int(input("  Harga min (0=dari Free): Rp ").strip())
            if harga_min >= 0:
                break
            print("  ❌ Tidak boleh negatif.")
        except ValueError:
            print("  ❌ Masukkan angka bulat.")

    while True:
        try:
            raw = int(input("  Harga maks (0=tak terbatas): Rp ").strip())
            if raw < 0:
                print("  ❌ Tidak boleh negatif.")
                continue
            harga_maks = float('inf') if raw == 0 else raw
            break
        except ValueError:
            print("  ❌ Masukkan angka bulat.")

    if harga_maks != float('inf') and harga_min > harga_maks:
        print("  ⚠️  Harga min > maks, otomatis dibalik.")
        harga_min, harga_maks = harga_maks, harga_min

    return genre_hasil, harga_min, harga_maks


# ============================================================
# PIPELINE REKOMENDASI
# ============================================================
def jalankan_rekomendasi(genre_user, harga_min, harga_maks):
    """
    Menjalankan pipeline lengkap BFS -> Dijkstra -> SAW
    dari genre dan filter harga yang sudah ditentukan.
    """
    # STEP 1: Bangun Graph Genre
    print("\n[1/5] Membangun Graph Genre...")
    graph_genre, adjacency_genre = bangun_graph_genre(DATABASE_GAME)

    # STEP 2: BFS Cari Kandidat
    print("[2/5] BFS Traversal mencari kandidat game...")
    kandidat_ids = set()
    # Jika All genre, BFS dari semua genre yang ada
    genre_bfs = SEMUA_GENRE if genre_user is None else genre_user
    for genre in genre_bfs:
        kandidat_ids.update(bfs_cari_kandidat(
            genre, graph_genre, adjacency_genre, kedalaman=2))

    # Terapkan filter harga pada kandidat (genre_filter=None karena sudah dihandle BFS)
    kandidat = terapkan_filter(
        [g for g in DATABASE_GAME if g["id"] in kandidat_ids],
        genre_filter=None,
        harga_min=harga_min,
        harga_maks=harga_maks
    )
    kandidat_ids = {g["id"] for g in kandidat}

    if not kandidat_ids:
        print("\n❌  Tidak Ada Data — Tidak ditemukan game yang sesuai preferensi & budget.")
        return None, None

    print(f"     -> Ditemukan {len(kandidat_ids)} kandidat game")

    # STEP 3: Bangun Graph Kemiripan
    print("[3/5] Membangun Graph Kemiripan antar game...")
    graph_kemiripan, id_to_game = bangun_graph_kemiripan(
        kandidat_ids, DATABASE_GAME)

    # STEP 4: Dijkstra — titik acuan = game dengan genre paling cocok
    print("[4/5] Dijkstra menghitung jarak kemiripan...")
    if genre_user is None:
        # All genre: pakai game dengan popularitas tertinggi sebagai titik acuan
        start_id = max(
            kandidat_ids, key=lambda gid: id_to_game[gid]["popularitas"])
    else:
        start_id = max(
            kandidat_ids,
            key=lambda gid: len(
                set(id_to_game[gid]["genre"]) & set(genre_user))
        )
    dist_kemiripan = dijkstra(graph_kemiripan, start_id, kandidat_ids)

    # STEP 5: SAW
    print("[5/5] Menghitung SAW dan ranking...")
    hasil = hitung_saw([id_to_game[gid]
                       for gid in kandidat_ids], dist_kemiripan)

    return hasil, dist_kemiripan


# ============================================================
# MENU UTAMA
# ============================================================
def menu_utama():
    tampilkan_header()
    print(f"\n  Bobot SAW (otomatis): Rating={BOBOT_SAW['rating']} | "
          f"Harga={BOBOT_SAW['harga']} | "
          f"Popularitas={BOBOT_SAW['popularitas']} | "
          f"Kemiripan={BOBOT_SAW['kemiripan']}")

    while True:
        print("\n" + "="*40)
        print("  MENU UTAMA")
        print("="*40)
        print("  1. Lihat Katalog Game")
        print("  2. Rekomendasi & Filter Game")
        print("  3. Keluar")

        pilihan = input("\nPilih menu (1-3): ").strip()

        # ── Menu 1: Lihat Katalog ────────────────────────────
        if pilihan == "1":
            tampilkan_katalog(DATABASE_GAME)

        # ── Menu 2: Rekomendasi & Filter ─────────────────────
        elif pilihan == "2":
            genre_filter, harga_min, harga_maks = input_preferensi()

            batas_min_str = "Free (Rp 0)" if harga_min == 0 else f"Rp {harga_min:,}"
            batas_maks_str = "Tidak terbatas" if harga_maks == float(
                'inf') else f"Rp {harga_maks:,}"
            label_genre = "Semua Genre" if genre_filter is None else ", ".join(
                genre_filter)
            print(f"\n✅  Genre   : {label_genre}")
            print(f"✅  Budget  : {batas_min_str} s/d {batas_maks_str}")

            hasil, dist_kemiripan = jalankan_rekomendasi(
                genre_filter, harga_min, harga_maks)
            if hasil is None:
                continue

            tampilkan_rekomendasi(hasil)

            lihat_detail = input(
                "\nLihat detail matriks keputusan? (y/n): ").strip().lower()
            if lihat_detail == 'y':
                print("\n📊  DETAIL MATRIKS KEPUTUSAN (semua kandidat)")
                print(
                    f"{'Rank':<5} {'ID':<5} {'Nama':<28} {'Rating':>7} {'Harga':>14} {'Pop':>5} {'Jarak':>7} {'Skor':>8}")
                print("-"*80)
                for item in hasil:
                    d = dist_kemiripan.get(item["id"], 999)
                    print(f"{item['rank']:<5} {item['id']:<5} {item['nama']:<28} "
                          f"{item['rating']:>7.1f} {fmt_harga(item['harga']):>14} "
                          f"{item['popularitas']:>5} {d:>7.4f} {item['skor_saw']:>8.4f}")

        # ── Menu 3: Keluar ────────────────────────────────────
        elif pilihan == "3":
            print("\n👋  Terima kasih telah menggunakan DSS Game Catalog. Sampai jumpa!")
            break

        else:
            print("❌  Pilihan tidak valid. Masukkan 1-3.")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    menu_utama()
