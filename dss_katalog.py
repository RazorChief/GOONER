"""
DSS Katalog Rekomendasi Game
Berdasarkan Genre & Harga
Menggunakan: BFS Graph Traversal + Dijkstra + SAW (Simple Additive Weighting)
"""

from collections import defaultdict, deque
import heapq


# ============================================================
# DATABASE GAME — Node sesuai laporan (G1–G20)
# Harga "Free" → 0
# ============================================================
DATABASE_GAME = [
    {"id": "G1",  "nama": "Minecraft",                  "genre": [
        "Sandbox"],       "harga": 538000, "rating": 9.0, "popularitas": 98},
    {"id": "G2",  "nama": "Terraria",                   "genre": [
        "Sandbox"],       "harga": 90000,  "rating": 9.2, "popularitas": 91},
    {"id": "G3",  "nama": "Stardew Valley",             "genre": [
        "Simulation"],    "harga": 115000, "rating": 9.0, "popularitas": 88},
    {"id": "G4",  "nama": "Hollow Knight",              "genre": [
        "Action"],        "harga": 130000, "rating": 9.1, "popularitas": 85},
    {"id": "G5",  "nama": "Hades II",                   "genre": [
        "Action"],        "harga": 245000, "rating": 9.4, "popularitas": 90},
    {"id": "G6",  "nama": "Valorant",                   "genre": [
        "Shooter"],       "harga": 0,      "rating": 8.5, "popularitas": 95},
    {"id": "G7",  "nama": "Tekken",                     "genre": [
        "Fighting"],      "harga": 799000, "rating": 8.8, "popularitas": 82},
    {"id": "G8",  "nama": "Dragon Ball Xenoverse",      "genre": [
        "Fighting"],      "harga": 450000, "rating": 8.3, "popularitas": 78},
    {"id": "G9",  "nama": "Satisfactory",               "genre": [
        "Sandbox"],       "harga": 210000, "rating": 8.9, "popularitas": 84},
    {"id": "G10", "nama": "Zomboid",                    "genre": [
        "Shooter"],       "harga": 139000, "rating": 8.7, "popularitas": 80},
    {"id": "G11", "nama": "Fishing Simulator",          "genre": [
        "Simulation"],    "harga": 0,      "rating": 7.5, "popularitas": 65},
    {"id": "G12", "nama": "7 Days to Die",              "genre": [
        "Sandbox"],       "harga": 338000, "rating": 8.2, "popularitas": 76},
    {"id": "G13", "nama": "Wuthering Wave",             "genre": [
        "RPG"],           "harga": 0,      "rating": 8.6, "popularitas": 87},
    {"id": "G14", "nama": "Blue Archive",               "genre": [
        "RPG"],           "harga": 0,      "rating": 8.4, "popularitas": 83},
    {"id": "G15", "nama": "Marvel Rivals",              "genre": [
        "Action"],        "harga": 0,      "rating": 8.5, "popularitas": 89},
    {"id": "G16", "nama": "House Flipper",              "genre": [
        "Simulation"],    "harga": 206000, "rating": 8.3, "popularitas": 72},
    {"id": "G17", "nama": "Subnautica",                 "genre": [
        "Sandbox"],       "harga": 350000, "rating": 9.1, "popularitas": 88},
    {"id": "G18", "nama": "Devil May Cry 5",            "genre": [
        "Action"],        "harga": 389000, "rating": 9.0, "popularitas": 86},
    {"id": "G19", "nama": "Limbus Company",             "genre": [
        "RPG"],           "harga": 0,      "rating": 8.7, "popularitas": 81},
    {"id": "G20", "nama": "Umamusume: Pretty Derby",    "genre": [
        "Simulation"],    "harga": 0,      "rating": 8.2, "popularitas": 75},
]

# ============================================================
# EDGE sesuai laporan:
#   - Genre sama  → jarak kemiripan rendah  (0.1)
#   - Harga mirip → jarak kemiripan sedang  (0.3)
# Edge bersifat undirected (dua arah)
# ============================================================
EDGES_LAPORAN = [
    # (node_awal, node_tujuan, keterangan, bobot_jarak)
    ("G1",  "G2",  "Genre sama",   0.1),
    ("G2",  "G3",  "Harga mirip",  0.3),
    ("G3",  "G4",  "Harga mirip",  0.3),
    ("G4",  "G5",  "Genre sama",   0.1),
    ("G5",  "G6",  "Harga mirip",  0.5),   # Action ↔ Shooter (lebih jauh)
    ("G6",  "G10", "Genre sama",   0.1),   # Shooter ↔ Shooter
    ("G7",  "G8",  "Genre sama",   0.1),   # Fighting ↔ Fighting
    ("G8",  "G9",  "Harga mirip",  0.3),
    ("G9",  "G12", "Genre sama",   0.1),   # Sandbox ↔ Sandbox
    ("G1",  "G9",  "Genre sama",   0.1),   # Sandbox ↔ Sandbox
    ("G1",  "G12", "Genre sama",   0.1),
    ("G1",  "G17", "Genre sama",   0.1),
    ("G2",  "G9",  "Genre sama",   0.1),
    ("G2",  "G12", "Genre sama",   0.1),
    ("G2",  "G17", "Genre sama",   0.1),
    ("G9",  "G17", "Genre sama",   0.1),
    ("G12", "G17", "Genre sama",   0.1),
    ("G3",  "G11", "Genre sama",   0.1),   # Simulation ↔ Simulation
    ("G3",  "G16", "Genre sama",   0.1),
    ("G3",  "G20", "Genre sama",   0.1),
    ("G11", "G16", "Genre sama",   0.1),
    ("G11", "G20", "Genre sama",   0.1),
    ("G16", "G20", "Genre sama",   0.1),
    ("G13", "G14", "Genre sama",   0.1),   # RPG ↔ RPG
    ("G13", "G19", "Genre sama",   0.1),
    ("G14", "G19", "Genre sama",   0.1),
    ("G4",  "G15", "Genre sama",   0.1),   # Action ↔ Action
    ("G4",  "G18", "Genre sama",   0.1),
    ("G5",  "G15", "Genre sama",   0.1),
    ("G5",  "G18", "Genre sama",   0.1),
    ("G15", "G18", "Genre sama",   0.1),
    ("G3",  "G20", "Harga mirip",  0.3),   # ujung sesuai tabel laporan
]

SEMUA_GENRE = sorted(set(g for game in DATABASE_GAME for g in game["genre"]))


# ============================================================
# STEP 1: BANGUN GRAPH GENRE (Genre -> List Game)
# ============================================================
def bangun_graph_genre(database):
    """
    Node  = Genre
    Edge  = koneksi antar genre berdasarkan EDGES_LAPORAN
    Setiap genre -> list game_id yang memiliki genre tersebut
    """
    graph = defaultdict(list)    # genre -> [game_id, ...]
    adjacency = defaultdict(set)  # genre -> {genre tetangga}

    id_to_game = {g["id"]: g for g in database}

    # Isi graph genre -> game
    for game in database:
        for genre in game["genre"]:
            graph[genre].append(game["id"])

    # Bangun adjacency berdasarkan EDGES_LAPORAN
    for (u, v, ket, _) in EDGES_LAPORAN:
        gu = id_to_game[u]["genre"][0]
        gv = id_to_game[v]["genre"][0]
        adjacency[gu].add(gv)
        adjacency[gv].add(gu)

    return graph, adjacency


# ============================================================
# STEP 2: BFS – Cari Kandidat Game Berdasarkan Genre
# ============================================================
def bfs_cari_kandidat(start_genre, graph_genre, adjacency, kedalaman=2):
    """
    BFS dari genre yang dipilih user.
    Jelajahi genre tetangga hingga kedalaman tertentu
    untuk mendapatkan kandidat game yang relevan.
    """
    visited_genre = set()
    queue = deque([(start_genre, 0)])
    kandidat_ids = set()

    while queue:
        genre, depth = queue.popleft()

        if genre in visited_genre or depth > kedalaman:
            continue
        visited_genre.add(genre)

        # Tambahkan game dari genre ini
        if genre in graph_genre:
            for gid in graph_genre[genre]:
                kandidat_ids.add(gid)

        # Jelajahi genre tetangga (kedalaman +1)
        if depth < kedalaman:
            for tetangga in adjacency.get(genre, []):
                if tetangga not in visited_genre:
                    queue.append((tetangga, depth + 1))

    return kandidat_ids


# ============================================================
# STEP 3: BANGUN GRAPH KEMIRIPAN ANTAR GAME (dari EDGES_LAPORAN)
# ============================================================
def hitung_kemiripan_genre(game_a, game_b):
    """Jaccard Similarity -> jarak (cost)."""
    set_a = set(game_a["genre"])
    set_b = set(game_b["genre"])
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 1.0
    return round(1.0 - intersection / union, 4)


def bangun_graph_kemiripan(kandidat_ids, database):
    """
    Weighted graph kemiripan antar game kandidat.
    Prioritas bobot: gunakan edge eksplisit dari EDGES_LAPORAN (sesuai laporan),
    fallback ke Jaccard similarity untuk pasangan yang tidak ada di laporan.
    """
    id_to_game = {g["id"]: g for g in database}
    graph = defaultdict(list)  # game_id -> [(bobot, game_id_lain)]

    # Indeks cepat edge laporan (undirected)
    edge_index = {}
    for (u, v, ket, bobot) in EDGES_LAPORAN:
        edge_index[(u, v)] = bobot
        edge_index[(v, u)] = bobot

    ids = list(kandidat_ids)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if (a, b) in edge_index:
                bobot = edge_index[(a, b)]
            else:
                # Fallback Jaccard untuk pasangan yang tidak ada di laporan
                bobot = hitung_kemiripan_genre(id_to_game[a], id_to_game[b])
            graph[a].append((bobot, b))
            graph[b].append((bobot, a))

    return graph, id_to_game


# ============================================================
# STEP 4: DIJKSTRA – Hitung Jarak Kemiripan dari Game Referensi
# ============================================================
def dijkstra(graph, start_id, kandidat_ids):
    """
    Dijkstra dari node start_id (game acuan).
    Menghitung jarak kemiripan minimum ke semua game kandidat.
    Jarak kecil = sangat mirip dengan preferensi user.
    """
    dist = {gid: float('inf') for gid in kandidat_ids}
    dist[start_id] = 0
    pq = [(0, start_id)]  # (jarak, node)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for (w, v) in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist


# ============================================================
# STEP 5: BENTUK MATRIKS KEPUTUSAN & SAW
# ============================================================
def normalisasi_benefit(nilai_list):
    """Normalisasi benefit: nilai / max"""
    max_val = max(nilai_list) if max(nilai_list) != 0 else 1
    return [v / max_val for v in nilai_list]


def normalisasi_cost(nilai_list):
    """Normalisasi cost: min / nilai"""
    min_val = min(nilai_list) if min(nilai_list) != 0 else 1
    return [min_val / v if v != 0 else 0 for v in nilai_list]


def hitung_saw(games, dist_kemiripan, bobot):
    """
    SAW (Simple Additive Weighting).

    Kriteria:
      C1 - Rating      (benefit) – bobot diatur user
      C2 - Harga       (cost)    – bobot diatur user
      C3 - Popularitas (benefit) – bobot diatur user
      C4 - Kemiripan   (cost)    – bobot diatur user (dari Dijkstra)

    Mengembalikan list game dengan skor akhir.
    """
    n = len(games)
    if n == 0:
        return []

    ratings = [g["rating"] for g in games]
    harga = [g["harga"] for g in games]
    popularitas = [g["popularitas"] for g in games]
    kemiripan = [dist_kemiripan.get(g["id"], float('inf')) for g in games]

    # Ganti inf dengan max yang ada + 1 supaya tidak error
    max_k = max(k for k in kemiripan if k != float('inf')) + \
        1 if any(k != float('inf') for k in kemiripan) else 1
    kemiripan = [k if k != float('inf') else max_k for k in kemiripan]

    # Normalisasi
    norm_rating = normalisasi_benefit(ratings)
    norm_harga = normalisasi_cost(harga)
    norm_popularitas = normalisasi_benefit(popularitas)
    norm_kemiripan = normalisasi_cost(kemiripan)

    # Hitung nilai akhir SAW
    hasil = []
    for i, game in enumerate(games):
        skor = (
            bobot["rating"] * norm_rating[i] +
            bobot["harga"] * norm_harga[i] +
            bobot["popularitas"] * norm_popularitas[i] +
            bobot["kemiripan"] * norm_kemiripan[i]
        )
        hasil.append({**game, "skor_saw": round(skor, 4)})

    # Ranking
    hasil.sort(key=lambda x: x["skor_saw"], reverse=True)
    for rank, item in enumerate(hasil, 1):
        item["rank"] = rank

    return hasil


# ============================================================
# TAMPILAN HELPER
# ============================================================
def tampilkan_header():
    print("\n" + "="*60)
    print("  🎮  DSS KATALOG REKOMENDASI GAME  🎮")
    print("       Genre & Harga — BFS + Dijkstra + SAW")
    print("="*60)


def fmt_harga(h):
    return "Free" if h == 0 else f"Rp {h:>9,}"


def tampilkan_katalog(database):
    print("\n📋  KATALOG GAME TERSEDIA")
    print("-"*72)
    print(f"{'ID':<5} {'Nama Game':<30} {'Genre':<14} {'Harga':>12} {'Rating':>7}")
    print("-"*72)
    for g in database:
        genre_str = ", ".join(g["genre"])
        print(
            f"{g['id']:<5} {g['nama']:<30} {genre_str:<14} {fmt_harga(g['harga']):>12} {g['rating']:>7.1f}")
    print("-"*72)


def tampilkan_genre():
    print("\n🏷️   GENRE TERSEDIA:")
    for i, genre in enumerate(SEMUA_GENRE, 1):
        print(f"  {i:>2}. {genre}")


def input_genre_user():
    tampilkan_genre()
    print("\nPilih genre favorit Anda (pisahkan dengan koma, contoh: 1,3,5)")
    while True:
        try:
            pilihan = input("Pilihan genre: ").strip()
            indices = [int(x.strip()) - 1 for x in pilihan.split(",")]
            genre_dipilih = [SEMUA_GENRE[i]
                             for i in indices if 0 <= i < len(SEMUA_GENRE)]
            if genre_dipilih:
                return genre_dipilih
            print("❌ Pilihan tidak valid. Coba lagi.")
        except (ValueError, IndexError):
            print("❌ Input tidak valid. Masukkan angka yang tersedia.")


def input_budget_user():
    print("\n💰  ATUR BUDGET MAKSIMAL")
    print("  1. < Rp 100.000  (Budget hemat)")
    print("  2. < Rp 200.000  (Budget standar)")
    print("  3. < Rp 350.000  (Budget menengah)")
    print("  4. Tidak ada batas")
    while True:
        try:
            pilihan = int(input("Pilih budget (1-4): ").strip())
            budget_map = {1: 100000, 2: 200000, 3: 350000, 4: float('inf')}
            if pilihan in budget_map:
                return budget_map[pilihan]
            print("❌ Pilihan tidak valid.")
        except ValueError:
            print("❌ Masukkan angka 1-4.")


def input_bobot_user():
    print("\n⚖️   ATUR BOBOT KRITERIA (total harus = 1.0)")
    print("Kriteria: Rating | Harga | Popularitas | Kemiripan Genre")
    print("Contoh input: 0.4 0.3 0.2 0.1  (dipisah spasi)")
    while True:
        try:
            raw = input(
                "Bobot (Rating Harga Popularitas Kemiripan): ").strip().split()
            if len(raw) != 4:
                raise ValueError
            w = [float(x) for x in raw]
            if abs(sum(w) - 1.0) > 0.01:
                print(f"❌ Total bobot = {sum(w):.2f}, harus = 1.0")
                continue
            return {
                "rating":      w[0],
                "harga":       w[1],
                "popularitas": w[2],
                "kemiripan":   w[3],
            }
        except ValueError:
            print("❌ Format salah. Masukkan 4 angka desimal.")


def tampilkan_rekomendasi(hasil, top_n=5):
    print(f"\n🏆  TOP {top_n} REKOMENDASI GAME TERBAIK")
    print("="*75)
    print(f"{'Rank':<5} {'ID':<5} {'Nama Game':<28} {'Genre':<12} {'Harga':>12} {'Skor SAW':>9}")
    print("-"*75)
    for item in hasil[:top_n]:
        genre_str = ", ".join(item["genre"])
        print(f"  {item['rank']:<4} {item['id']:<5} {item['nama']:<28} {genre_str:<12} {fmt_harga(item['harga']):>12}  {item['skor_saw']:>8.4f}")
    print("="*75)


# ============================================================
# MENU UTAMA
# ============================================================
def menu_utama():
    tampilkan_header()

    while True:
        print("\n📌  MENU UTAMA")
        print("  1. Lihat Katalog Game")
        print("  2. Dapatkan Rekomendasi Game")
        print("  3. Filter Game Berdasarkan Harga")
        print("  4. Keluar")

        pilihan = input("\nPilih menu (1-4): ").strip()

        if pilihan == "1":
            # ---- USE CASE: Lihat Katalog Game ----
            tampilkan_katalog(DATABASE_GAME)

        elif pilihan == "2":
            # ---- USE CASE: Dapatkan Rekomendasi ----
            print("\n🔧  PENGATURAN PREFERENSI")

            genre_user = input_genre_user()
            budget_user = input_budget_user()
            bobot = input_bobot_user()

            print(f"\n✅  Genre pilihan  : {', '.join(genre_user)}")
            print(
                f"✅  Budget maks    : {'Tidak terbatas' if budget_user == float('inf') else f'Rp {budget_user:,.0f}'}")

            # === STEP 1: Bangun Graph Genre ===
            print("\n⚙️  [1/5] Membangun Graph Genre...")
            graph_genre, adjacency_genre = bangun_graph_genre(DATABASE_GAME)

            # === STEP 2: BFS Cari Kandidat ===
            print("⚙️  [2/5] BFS Traversal mencari kandidat game...")
            kandidat_ids = set()
            for genre in genre_user:
                ids = bfs_cari_kandidat(
                    genre, graph_genre, adjacency_genre, kedalaman=2)
                kandidat_ids.update(ids)

            # Filter berdasarkan budget
            id_to_game = {g["id"]: g for g in DATABASE_GAME}
            # harga 0 = Free, selalu lolos filter
            kandidat_ids = {
                gid for gid in kandidat_ids if id_to_game[gid]["harga"] == 0 or id_to_game[gid]["harga"] <= budget_user}

            if not kandidat_ids:
                print(
                    "\n❌  Tidak Ada Data — Tidak ditemukan game yang sesuai preferensi & budget Anda.")
                continue

            print(f"    → Ditemukan {len(kandidat_ids)} kandidat game")

            # === STEP 3: Bangun Graph Kemiripan ===
            print("⚙️  [3/5] Membangun Graph Kemiripan antar game...")
            graph_kemiripan, id_to_game = bangun_graph_kemiripan(
                kandidat_ids, DATABASE_GAME)

            # === STEP 4: Dijkstra ===
            print("⚙️  [4/5] Dijkstra menghitung jarak kemiripan...")
            # Gunakan game dengan genre yang paling banyak cocok sebagai titik acuan
            start_id = max(
                kandidat_ids,
                key=lambda gid: len(
                    set(id_to_game[gid]["genre"]) & set(genre_user))
            )
            dist_kemiripan = dijkstra(graph_kemiripan, start_id, kandidat_ids)

            # === STEP 5: Matriks Keputusan + SAW ===
            print("⚙️  [5/5] Menghitung SAW dan ranking...")
            games_kandidat = [id_to_game[gid] for gid in kandidat_ids]
            hasil = hitung_saw(games_kandidat, dist_kemiripan, bobot)

            # Tampilkan rekomendasi
            tampilkan_rekomendasi(hasil, top_n=min(5, len(hasil)))

            # Detail matriks (opsional)
            lihat_detail = input(
                "\nLihat detail matriks keputusan? (y/n): ").strip().lower()
            if lihat_detail == 'y':
                print("\n📊  DETAIL MATRIKS KEPUTUSAN")
                print(
                    f"{'No':<4} {'Nama':<28} {'Rating':>7} {'Harga':>10} {'Pop':>5} {'Jarak':>7} {'Skor':>8}")
                print("-"*70)
                for item in hasil:
                    d = dist_kemiripan.get(item["id"], 999)
                    print(f"{item['rank']:<4} {item['id']:<5} {item['nama']:<28} {item['rating']:>7.1f} {fmt_harga(item['harga']):>12} {item['popularitas']:>5} {d:>7.4f} {item['skor_saw']:>8.4f}")

        elif pilihan == "3":
            # ---- USE CASE: Filter Berdasarkan Harga ----
            budget = input_budget_user()
            # harga 0 = Free, selalu lolos filter budget
            filtered = [g for g in DATABASE_GAME if g["harga"]
                        == 0 or g["harga"] <= budget]

            if not filtered:
                print("\n❌  Tidak ada game dalam rentang harga tersebut.")
            else:
                print(f"\n🔍  GAME DENGAN HARGA ≤ Rp {budget:,.0f}")
                tampilkan_katalog(filtered)

        elif pilihan == "4":
            print("\n👋  Terima kasih telah menggunakan DSS Game Catalog. Sampai jumpa!")
            break

        else:
            print("❌  Pilihan tidak valid. Masukkan 1-4.")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    menu_utama()
