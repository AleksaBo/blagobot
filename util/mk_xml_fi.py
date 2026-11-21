import xml.etree.ElementTree as ET

# создание структуры
# main element

lst_day = []  # 7 days in day 7 chapts
lst_cpt = []    # 7 chapts Поклонение - Заключение
lst_artcl = [] # 1 - 8.9 ... aticls
lst_cont_artcl = []

#ствараем спіс элементаў - дні
def mk_main():
    mn_e = ET.Element('main')
    return mn_e

def mk_sub_day(day_val, perent_e):
    global lst_day
    for i in range(day_val):
        nm_e = "day" + str(i+1)
        lst_day.append(ET.SubElement(perent_e, nm_e))





def mk_data_str(root_e):
    
    ss = ET.tostring(root_e, encoding='unicode')
    return ss
    
    
def sv_fi_xml(path_fi, root_e):
    """_summary_

    Args:
        path_fi (_type_): путь к файлу
        
    """
    with open(path_fi, "w") as my_xml:
        my_xml.write(mk_data_str(root_e))
    


def main_def(pahh):
    mn_e = mk_main()
    mk_sub_day(7, mn_e)
    mk_data_str(mn_e)
    sv_fi_xml(pahh, mn_e)

if __name__ == "__main__":
    
    main_def('/home/saha_bo/Progy/pr_bot/bmpgo/bible_txt/myxml.xml')
    