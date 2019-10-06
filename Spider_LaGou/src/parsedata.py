# 数据清洗
COUNT = 1

def parse_data(json_data, url):
    global COUNT
    job_list = json_data["content"]["positionResult"]["result"]
    company_info = []
    # print(json_data)
    for job in job_list:
        print("正在解析第%s个信息岗位" % COUNT)
        job_info = {}
        for job_key, job_value in job.items():
            # companyFullName 公司全称
            # companySize 公司规模
            # financeStage 融资状况
            # district 位置
            # positionName  职位
            # workYear  工作经验要求
            # education 学历
            # salary 工资
            # positionAdvantage 福利待遇
            # companyLabelList  公司待遇
            # skillLables 技能要求
            # jobNature 工作性质，实习生或者全职
            # industryLables 行业标签
            # positionId 提取id构造职位页面请求
            if job_key in ['companyFullName', 'companySize', 'financeStage', 'district',
                           'positionName', 'workYear', 'education', 'salary', 'positionAdvantage',
                           'companyLabelList', 'skillLables', 'jobNature', 'industryLables']:
                job_info[job_key] = job_value
            if job_key == 'positionId':
                # print("%s%s.html" % (url, job_value))
                job_info["url"] = "%s%s.html" % (url, job_value)
        company_info.append(job_info)  # 把所有职位情况添加到网页信息page_info
        COUNT += 1
    return company_info
