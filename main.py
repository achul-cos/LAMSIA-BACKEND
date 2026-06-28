from tts import text_to_speech

obat = {
  'nama': 'Amlodipine',
  'dosis': '1 tablet',
  'kotak': 3
}

text = (
  "Selamat pagi."
  f"Saatnya minum obat {obat['nama']} dengan dosis{obat['dosis']}"
  f"Silahkan ambil pada kotak nomor {obat['kotak']}"
)

text_to_speech(text)
