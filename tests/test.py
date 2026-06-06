# query = "(((((amba1)/(amba2))/(amba3))/(amba4))/(amba5))"
# query = "(((username_like=bu)&(age>=18))/((status=aktif)))"
# where_query = "((((atribut1_like=X)&(atribut2>=Y)&(atribut3<=Z))/((atribut4=X)&(atribut5=Y)))/(atribut6=X))"
where_query = "(((username_like=bu)&(telephone==000000))/(telephone_like=123))"

from app.models.user_model import User

from sqlalchemy import and_, or_

def tokenize(q):
    tokens = []     # Wadah utama untuk menampung semua anggota '(', objek di dalam nest, ')'
    buffer = ""     # Wadah sementara untuk menampung objek di dalam nest

    # Looping setiap karakter pada query
    for char in q:

        # Jika karakter yang dilooping berupa '(', ')', atau '/'
        if char in "()/":

            """
            Pada saat melakukan looping karakter didalam query,
            Dan sampai di karakter berupa '(', ')', atau '/'
            Dilakukan pengecekan, apakah ada isi didalam wadah BUFFER
            Jika ada, pindahkan semua isi wadah BUFFER kedalam wadah TOKENS
            Setelah memindahkan semua isi wadah BUFFER, kosongkan lagi BUFFER nya
            """
            if buffer:
                tokens.append(buffer)
                buffer = ""

            """
            Tanpa validasi ini, isi wadah TOKEN hanyalah objek didalam nested,
            Sebagai contoh: ['amba', 'amba', 'amba', 'amba', 'amba']
            Sedangkan didalam objek nested memiliki tingkatan kedalaman nested nya,
            Cara mengetahu kedalaman nestednya dengan menyertakana juga karakter '(' dan ')'
            Didalam wadah atau list (array) sebagai anggota, yang mengapit objek nested
            Disini karakter '/' sudah tidak dibutuhkan, maka kita hanya perlu menangkap
            Karakter yang didalam '(', ')', dan '/', tapi tanpa '/' itu sendiri
            """
            if char != "/":
                tokens.append(char)
            
        # Selain karakter '(', ')', atau '/', karakter yang dilooping akan masuk kedalam wadah BUFFER
        else:
            buffer += char

    return tokens

def parse(tokens):
    stack = [[]]    # Wadah List Parsing Query
    i = 0           # Indexing Looping

    """
    Pada looping ini, setiap anggota di dalam list TOEKNS,
    yang merupakan perwarisan dari list TOKENS sebelum dengan anggota '(', objek di dalam nest, dan ')'
    akan diesekusi untuk diubah bentuknya menjadi nested list. Objek didalam nest tersebut
    akan dikurung didalam list, dimana kedalamannya mengikuti pada query, dengan menggunakan
    simbol '(' dan ')' untuk menentukan kedalaman suatu objek didalam nest.

    Looping dijalankan dengan logika jika nilai i (yang dideklarasikan sebelumnya yaitu i = 0)
    akan menjalankan fungsi didalam looping nya (while). Fungsi akan dijalankan terus menerus
    hingga nilai i sudah tidak lebih kecil dari jumlah anggota list tokens.

    Fungsi didalam looping dijalankan dimulai dengan mendeklarasikan sebuah variabel
    yang mendefinisikan sebuah anggota didalam list TOKENS pada urutan sesuai pada nilai i
    yang sedang dijalankan. Dan variabel tersebut kita sebut 't'...(1)

    Jika variabel 't' tersebut berupa '(', maka list STACK (sebagai wadah atau list dari
    query yang diparsing menjadi list) akan menambahkan sub wadah yang baru (sebelumnya
    list STACK sudah berisi satu sub wadah. Jadi jika fungsi ini baru dijalankan untuk
    pertama kali, harusnya menjadi stack = [[], []], yang sebelumnya stack = [[]]).
    Dan penambahan sub wadah yang baru akan dijalankan jika pada anggota list TOKENS selanjutnya
    tetap memenuhi validasi if t == "(":...(2)

    Tetapi jika variabel 't' tersebut berupa ')', maka dideklarasikan lah sebuah variabel
    GROUP yang mendefinisikan anggota paling terakhir dari list STACK.
    Contoh, STACK = [[x], [y], [z]], maka GROUP = [z]
    Tetapi secara bersamaan STACK kehilangan anggota paling terakhirnya, jadi proses ini bisa dibilang
    pemindahan anggota (sementara), maka STACK = [[x], [y]].
    Pemindahana anggota ini sementara, karena GROUP akan dimasukkan lagi kedalam list STACK pada
    anggota atau sub wadah yang palin terakhir, maka STACK = [[x], [y, [z]]]...
    Begitu terus, sampai looping selesai, hingga hasil akhir dari STACK harusnya menjadi,
    STACK = [[x, [y, [z]]]], Dapat ekspresikan sebagai berikut,
    STACK = [
        x,
        [
            y,
            [
                z
            ]
        ]
    ]...(3)

    Tetapi jika varibel 't' bukanlah '(' atau ')', maka dapat dipastikan itu merupakan anggota objek
    di dalam nest. Anggota tersebut dimasukkan pada list STACK pada sub wadah anggota paling terakhir. Contoh,
    sebelum, STACK = [[], [], []]
    t = [x]
    setelah, STACK = [[], [], [[x]]]...(4)

    Setelahnya fungsi dijalankan terus menerus hingga mengeksekusi semua anggota dari list TOKENS..(5)

    Setelah semua anggota dari list TOKENS telah dieksekusi untuk dilakukan parsing, hasil dari list STACK
    maka akan seperti ini, STACK = [[[[x, y], z]]]
    terdapat dua lapisan nested diatas yang perlu dihapus untuk menghasilkan satu list dengan satu lapis nest,
    maka kita dapat mengambil anggota pertama yang di dalam anggota pertama yang didalam list STACK, stack[0][0]
    maka hasilnya nanti,
    STACK = [[x, y], z]...(6)
    """
    while i < len(tokens):

        # (1) Deklarasi anggota list TOKENS pada urutan [i] sebagai sebuah variabel didalam looping
        t = tokens[i]

        # (2) Jika variabel t yaitu '(' maka pada list STACK akan menambahkan satu sub wadah terbaru
        if t == "(":
            stack.append([])

        # (3) Jika variabel t yaitu ')' maka anggota list STACK paling akhir akan dipindahkan pada anggota
        #     list STACK yang paling akhir kedua, dimana anggota list yang paling akhir kedua tersebut
        #     dianggap sebagai sub wadah, maka pemindaan anggota list STACK paling akhir menjadi anggota
        #     dari sub wadah atau list STACK yang paling akhir kedua.
        elif t == ")":
            group = stack.pop()
            stack[-1].append(group)

        # (4) Jika variabel t bukanlah '(' atau ')' maka variebel t dimasukkan pada list STACK pada anggota
        #     atau sub wadah paling terakhir.
        else:
            # value
            stack[-1].append(t)

        # (5) varibel i dinaikkan nilainya sebanyak 1 untuk mengeksekusi anggota list TOKENS selanjutnya
        i += 1

    # (6) Mengambil anggota pertama yang di dalam anggota pertama yang didalam list STACK
    return stack[0][0]



def query_and_parse(where_query):
    """
    Mengubah (parsing) where_query yang sebelumnya sudah di tokenize() oleh class query_tokenize, dan sudah di ubah
    (parsing) di query_or_parse(). Perubahan query yang sebelumnya, sebagai contoh:

    [[[['atribut1_like=X'], '&', ['atribut2>=Y'], '&', ['atribut3<=Z']], [['atribut4=X'], '&', ['atribut5=Y']]], ['atribut6=X']]

    List ini akan diubah bentuknya menjadi,
    [[('atribut1_like=X', 'atribut2>=Y', 'atribut3<=Z'), ('atribut4=X', 'atribut5=Y')], 'atribut6=X']

    Dilakukan penyederhanaan list, serta menghapus simbol '&' didalam list. Serta perubahan tipe data pada AND_GROUP menjadi tuple (x, y),
    serta pada OR_GROUP dilakukan penyesuaian menjadi list dengan bentuk [x, y]

    Parameters:
    where_query (list) : where_query yang telah di parsing menjadi bentuk AST untuk diubah bentuknya menjadi Database Query

    returns:
    list : where_query yang telah di parsing datanya, menjadi list yang lebih sederhana, perubahan tipe data AND_GROUP menjadi tuple
    dan penyesuaian OR_GROUP menjadi list.
    """

    # (1)   Validasi, jika parameter yang digunakan oleh fungsi berupa string,
    #       maka fungsi mengembalikan nilai parameter dan fungsi diselesaikan
    if isinstance(where_query, str):
        return where_query
    
    # (2)   Validasi, jika parameter yang digunakan oleh fungsi berupa list,
    #       maka jalankan kode di dalam validasi jika kondisi validasinya memenuhi.
    if isinstance(where_query, list):

        # (2.1) Validasi, jika parameter yang digunakan oleh fungsi, panjangnya berjumlah 1,
        #       maka jalankan fungsi query_and_parse() (fungsi ini sendiri) dengan parameternya,
        #       yaitu parameter dari fungsi ini dengan anggota ke-1 (indeks ke-0) dan mengembalikan
        #       hasil dari fungsinya
        if len(where_query) == 1:
            return query_and_parse(where_query[0])    


    # (3)   Validasi, jika parameter yang digunakan oleh fungsi berupa list,
    #       dan terdapat anggota dengan nilai '&' pada listnya,
    #       maka jalankan kode di dalam validasi jika kondisi validasinya memenuhi.
    if isinstance(where_query, list) and '&' in where_query:

        result = []     # List atau wadah untuk menampung hasil eksekusi anggota dari parameter pada looping (3.1)
                        # Setiap kali validasi (3) dijalankan, sekaligus mengosongkan isi dari list RESULT

        i = 0           # Index looping yang mengeksekusi setiap anggota dari parameter pada looping

        # (3.1) Looping, ketika nilai i (sebagai index looping) masih lebih kecil dari jumlah anggota parameter pada fungsi ini,
        #       maka jalankan looping
        while i < len(where_query):

            # (3.1.1)   Deklarasi, saat looping bekerja pada suatu nilai i tertentu, misal bernilai i,
            #           dideklarasikan anggota dari paremeter fungsi ini pada index yang bernilai i,
            #           anggota tersebut dideklarasikan pada variabel ITEM
            item = where_query[i]   

            # (3.1.2)   Validasi, jika nilai dari variabel ITEM bernilai '&' maka tingkatkan nlai i sejumlah 1,
            #           dan lanjutkan atau kembalikan lagi ke (3.1)
            if item == '&':
                i += 1
                continue

            # (3.1.3)   Eksekusi, variabel ITEM berupa suatu anggota dari paremeter fungsi ini pada index [i]
            #           akan menjadi parmeter dari fungsi query_and_parse() (fungsi ini sendiri) dimana parameter
            #           fungsi itu yaitu variabel item. Hasil dari eksekusi fungsi ini dikembalikan, diterima, dan
            #           dimasukkan kedalam list RESULT. Setelahnya, nilai dari i dijumlahkan sebanyak 1
            result.append(query_and_parse(item))
            i += 1

        # (3.2) Return, setelah looping yang dilakukan pada (3.1) 
        #       list RESULT yang menerima nilai dari eksekusi looping dari setiap anggota dari paremeter fungsi ini,
        #       akan diubah tipe datanya menjadi tuple (x, y). Serta mengembalikan nilai RESULT hasil dari eksekusi
        #       dari fungsi ini.
        return tuple(result)

    # (4)   Validasi, jika parameter yang digunakan oleh fungsi berupa list,
    #       dan tidak ada anggota didalam list tersebut bernilai '&',
    #       maka jalankan kode di dalam validasi jika kondisi validasinya memenuhi. 
    if isinstance(where_query, list) and '&' not in where_query:

        result = []     # List atau wadah untuk menampung hasil eksekusi anggota dari parameter pada looping (3.1)
                        # Setiap kode di dalam validasi ini dijalankan, dia akan mengosongkan isi list dari RESULT

        # (4.1) Looping, Pada setiap anggota didalam list parameter fungsi ini,
        #       maka jalankan kode didalam looping ini dengan variabel ITEM yang mewakili anggota yang dieksekusi,
        #       serta dilakukan sebanyak jumlah anggota dari list parameter fungsi ini.
        for item in where_query:

            # (4.1.1)   Deklarasi, variabel simplified mendefinisikan nilainya sebagai hasil dari eksekusi fungsi
            #           query_and_parse() (fungsi ini sendiri) dimana parameter dari fungsinya yaitu variabel ITEM
            simplified = query_and_parse(item)

            # (4.1.2)   Eksekusi, list RESULT akan memasukkan variabel simplified kedalam list,
            #           dan menjadikanya sebagai anggota.
            result.append(simplified)

        # (4.2) Return, mengembalikan nilai dari hasil eksekusi kode di dalam validasi (4) berupa nilai dari RESULT
        return result

# [
#   [
#       ('atribut1_like=X', 'atribut2>=Y', 'atribut3<=Z'), 
#       ('atribut4=X', 'atribut5=Y')
#   ], 
#   'atribut6=X'
#]

def query_parse_sqlalchemy_expression(model, query):

    if query is None:
            return None    

    if isinstance(query, str):
        return operator_parser(model, query)
    
    if isinstance(query, tuple):
        return and_(*[
            operator_parser(model, q) for q in query
        ])
    
    if isinstance(query, list):
        
        if len(query) == 1:
            return query_parse_sqlalchemy_expression(model, query[0])           

        OR_GROUP = []

        for q in query:
            expr = query_parse_sqlalchemy_expression(model, q)

            if expr is not None:
                OR_GROUP.append(expr)

    if not OR_GROUP:
        return None

    return or_(*OR_GROUP)

def operator_parser(model, atr):

    if "_like=" in atr:
        field, value = atr.split("_like=")
        return getattr(model, field).like(f"%{value}%")
    
    if "_in=" in atr:
        field, value = atr.split("_in=")
        values = value.split(",")
        return getattr(model, field).in_(values)
    
    if "_not_in=" in atr:
        field, value = atr.split("_not_in=")
        values = value.split(",")
        return ~getattr(model, field).in_(values)

    if "_between=" in atr:
        field, value = atr.split("_between=")
        start, end = value.split(",")
        return getattr(model, field).beetwen(start, end)
    
    if "_not_between=" in atr:
        field, value = atr.split("_not_between=")
        start, end = value.split(",")
        return ~getattr(model, field).beetwen(start, end)
    
    if ">=" in atr:
        field, value = atr.split(">=")
        return getattr(model, field) >= value
    
    if "<=" in atr:
        field, value = atr.split("<=")
        return getattr(model, field) <= value
    
    if "!=" in atr:
        field, value = atr.split("!=")
        return getattr(model, field) != value
    
    if ">" in atr:
        field, value = atr.split(">")
        return getattr(model, field) > value
    
    if "<" in atr:
        field, value = atr.split("<")
        return getattr(model, field) < value
    
    if "==" in atr:
        field, value = atr.split("==")
        return getattr(model, field) == value    

# print(query_and_parse(parse(tokenize(where_query))))

# print(tokenize(query))

# simplify(parse(tokenize(query)))

# print(parse(tokenize(query)))

print(query_parse_sqlalchemy_expression(User, query_and_parse(parse(tokenize(where_query)))))