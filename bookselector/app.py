from flask import Flask, render_template, request, redirect, url_for, session, flash
from data.book_data import library_tree, find_book_by_title, search_books_tree, sort_books
import time

app = Flask(__name__)
app.secret_key = 'apaajalah'

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = ""
    search_results = None
    search_time = None
    sort_by = "judul"
    sort_order = "asc"
    if "peminjaman" not in session:
        session["peminjaman"] = []

    if request.method == "POST":
        if 'pinjam' in request.form:
            buku_judul = request.form['pinjam']
            if buku_judul not in session["peminjaman"]:
                session["peminjaman"].append(buku_judul)
                session.modified = True
                flash(f"Buku '{buku_judul}' berhasil dipinjam!")
            return redirect(url_for('index'))

        elif 'batal' in request.form:
            buku_judul = request.form['batal']
            if buku_judul in session["peminjaman"]:
                session["peminjaman"].remove(buku_judul)
                session.modified = True
                flash(f"Peminjaman buku '{buku_judul}' berhasil dibatalkan!")
            return redirect(url_for('index'))

        elif 'search' in request.form:
            keyword = request.form.get("keyword", "").strip()
            sort_by = request.form.get("sort_by", "judul")
            sort_order = request.form.get("sort_order", "asc")
            start_time = time.time()
            search_results = search_books_tree(keyword)
            search_results = sort_books(search_results, sort_by, sort_order)
            search_time = round((time.time() - start_time) * 1000, 2)

    return render_template(
        "index.html",
        library_tree=library_tree,
        peminjaman=session["peminjaman"],
        keyword=keyword,
        search_results=search_results,
        search_time=search_time,
        sort_by=sort_by,
        sort_order=sort_order
    )

@app.route("/pinjaman")
def pinjaman():
    pinjam_list = []
    for judul in session.get("peminjaman", []):
        buku = find_book_by_title(judul)
        if buku:
            pinjam_list.append(buku)
    
    return render_template("pinjaman.html", pinjam_list=pinjam_list)

if __name__ == "__main__":
    app.run(debug=True)
