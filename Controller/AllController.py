import requests
from urllib.parse import quote
from datetime import datetime


class ReadUrl:

  def read_json(self, url):
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
    return None


# ============ STUDENTS ============================
class STUDENTS:

  def _format_date(self, date_str):
    try:
      date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
      return date_obj.strftime("%A, %d %B %Y")
    except Exception:
      return "No Data"

  def GetStudentDetail(self, student_id):
    reader = ReadUrl()
    detail_url = f'https://api-frontend.kemdikbud.go.id/detail_mhs/{student_id}'
    student_details = reader.read_json(detail_url)
    # Check if tgl_keluar exists in dataumum
    if 'tgl_keluar' in student_details['dataumum']:
      tgl_keluar = student_details['dataumum']['tgl_keluar']
      formatted_date = self._format_date(tgl_keluar)
      student_details['dataumum']['tgl_keluar'] = formatted_date

    return student_details

  def GetMhsList(self, search_name=None):
    reader = ReadUrl()
    url = 'https://api-frontend.kemdikbud.go.id/hit_mhs/'
    if search_name:
      encoded_search_name = quote(search_name)
      url += encoded_search_name
    #print('iniiiii url ', url)
    getmhs_list = reader.read_json(url)
    #print("hhe list mhs", getmhs_list)
    if getmhs_list is None:
      return []

    if "Cari kata kunci" in getmhs_list.get("mahasiswa", [])[0]["text"]:
      return [{"text": getmhs_list["mahasiswa"][0]["text"]}]

    filtered_students = []
    for student in getmhs_list.get("mahasiswa", []):
      # this for more specify
      #if search_name and search_name.lower() not in student["text"].lower():
      #  continue
      info = student["text"].split(", ")
      name = info[0].split("(")[0]
      id_number = info[0].split("(")[1].split(")")[0]
      college = info[1].split(" : ")[1]
      program = info[2].split(": ")[1]
      link = student["website-link"]
      link = link.replace("/data_mahasiswa", "")
      filtered_students.append({
          "name": name,
          "id_number": id_number,
          "college": college,
          "program": program,
          "website-link": link
      })

    return filtered_students