from openpyxl import Workbook


def add_student_grades(filename):
    try:
        # 创建一个新的工作簿或打开已有的工作簿
        workbook = Workbook()
        sheet = workbook.active

        # 添加表头
        sheet.append(['学生姓名', '语文成绩'])

        while True:
            # 获取学生姓名和语文成绩的输入
            student_name = input("请输入学生姓名（输入 q 退出录入）：")

            # 如果用户输入 'q'，则退出循环
            if student_name.lower() == 'q':
                break

            chinese_score = input(f"请输入学生 {student_name} 的语文成绩：")

            # 添加新的学生姓名和语文成绩
            sheet.append([student_name, chinese_score])
            print(f"学生 {student_name} 的语文成绩 {chinese_score} 已成功录入。")

        # 保存文件
        workbook.save(filename)
        print(f"所有学生信息已成功录入到 {filename} 文件中。")

    except Exception as e:
        print(f"录入数据时出现错误：{e}")


# 示例用法
if __name__ == "__main__":
    filename = "student_grades.xlsx"
    add_student_grades(filename)
