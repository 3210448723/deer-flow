import pandas as pd
import numpy as np
from typing import Annotated
from langchain_core.tools import tool
from src.tools.decorators import log_io

nan = np.nan
import os
from src.tools.decorators import exception_handler

cache_dir = "/home/user/yuanjinmin/langgraph/deer-flow/src/rag/law/cache/"
os.makedirs(cache_dir, exist_ok=True)

dataset_path = "src/rag/law/law_dataset_1202.xlsx"


def load_data_with_cache():
    cache_file = os.path.join(cache_dir, "data.pkl")
    if os.path.exists(cache_file):
        print("从缓存加载数据...")
        return pd.read_pickle(cache_file)
    else:
        print("加载数据中...")
        data = {
            "company_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='company_info'),
            "company_register": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='company_register'),
            "sub_company_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='sub_company_info'),
            "legal_document": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='legal_doc'),
            "court_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='court_info'),
            "court_code": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='court_code'),
            "lawfirm_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='lawfirm_info'),
            "lawfirm_log": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='lawfirm_log'),
            "address_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='addr_info'),
            "legal_abstract": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='legal_abstract'),
            "restriction_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='restriction_case'),
            "finalized_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='finalized_case'),
            "dishonesty_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='dishonesty_case'),
            "administrative_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='administrative_case')
        }
        pd.to_pickle(data, cache_file)
        print("数据加载完成并已缓存")
        return data


# 加载数据
data = load_data_with_cache()
company_info = data["company_info"]
company_register = data['company_register']
sub_company_info = data['sub_company_info']
legal_document = data['legal_document']
court_info = data['court_info']
court_code = data['court_code']
lawfirm_info = data['lawfirm_info']
lawfirm_log = data['lawfirm_log']
address_info = data['address_info']
legal_abstract = data['legal_abstract']
restriction_case = data['restriction_case']
finalized_case = data['finalized_case']
dishonesty_case = data['dishonesty_case']
administrative_case = data['administrative_case']

@tool
@log_io
@exception_handler
def get_company_info(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【公司名称、公司简称或公司代码】查找【上市公司】信息
    {
    '公司名称': '上海妙可蓝多食品科技股份有限公司',
    '公司简称': '妙可蓝多',
    '英文名称': 'Shanghai Milkground Food Tech Co., Ltd.',
    '关联证券': nan,
    '公司代码': 600882,
    '曾用简称': '大成股份>> *ST大成>> 华联矿业>> 广泽股份',
    '所属市场': '上交所',
    '所属行业': '食品制造业',
    '成立日期': '1988-11-29',
    '上市日期': '1995-12-06',
    '法人代表': '柴琇',
    '总经理': '柴琇',
    '董秘': '谢毅',
    '邮政编码': 200136,
    '注册地址': '上海市奉贤区工业路899号8幢',
    '办公地址': '上海市浦东新区金桥路1398号金台大厦10楼',
    '联系电话': '021-50188700',
    '传真': '021-50188918',
    '官方网址': 'www.milkground.cn',
    '电子邮箱': 'ir@milkland.com.cn',
    '入选指数': '国证Ａ指,巨潮小盘',
    '主营业务': '',
    '经营范围': '',
    '机构简介': '',
    '每股面值': 1.0,
    '首发价格': 1.0,
    '首发募资净额': 4950.0,
    '首发主承销商': nan}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    company_info['公司代码'] = company_info['公司代码'].astype(str)
    row = company_info[(company_info['公司名称'] == identifier) |
                       (company_info['公司简称'] == identifier) |
                       (company_info['公司代码'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}
@tool
@log_io
@exception_handler
def get_company_register(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【公司名称】查询【工商】信息
    {
    '公司名称': '天能电池集团股份有限公司',
    '登记状态': '妙可蓝多',
    '统一社会信用代码': '913305007490121183',
    '法定代表人': '',
    '注册资本': 97210.0,
    '成立日期': '2003-03-13',
    '联系地址': '',
    '联系电话': '',
    '联系邮箱': '',
    '注册号': '330500400001780',
    '组织机构代码': '74901211-8',
    '参保人数': 709,
    '行业一级': '',
    '行业二级': '',
    '行业三级': '',
    '曾用名': '天能电池集团有限公司、浙江天能电池有限公司',
    '企业简介': '',
    '经营范围': ''}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = company_register[(company_register['公司名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_company_register_name(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【统一社会信用代码】查询【公司名称】
    {
    '公司名称': '天能电池集团股份有限公司',
    '登记状态': '妙可蓝多',
    '统一社会信用代码': '913305007490121183',
    '注册资本': 97210.0,
    '成立日期': '2003-03-13',
    '省份': '浙江省',
    '城市': '湖州市',
    '区县': '长兴县',
    '注册号': '330500400001780',
    '组织机构代码': '74901211-8',
    '参保人数': 709,
    '企业类型': '其他股份有限公司（上市）',
    '曾用名': '天能电池集团有限公司、浙江天能电池有限公司'}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = company_register[(company_register['统一社会信用代码'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()['公司名称']
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()['公司名称']
    else:
        return "No data found for the specified identifier."


@tool
@log_io
@exception_handler
def get_sub_company_info(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【被投资的公司名称】查询【母公司及投资】信息
    {
    '关联上市公司全称': '',
    '上市公司关系': '',
    '上市公司参股比例': '',
    '上市公司投资金额': ‘’,
    '公司名称': ‘’}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = sub_company_info[(sub_company_info['公司名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_sub_company_info_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【母公司的名称】查询所有【投资的子公司信息】
    {
    '关联上市公司全称': '',
    '上市公司关系': '',
    '上市公司参股比例': '',
    '上市公司投资金额': ‘’,
    '子公司名称': ‘’}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = sub_company_info[(sub_company_info['关联上市公司全称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_legal_document(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【案号】查询【裁判文书】结构化相关信息
    {
    '关联公司': '',
    '标题': '',
    '案号': '',
    '文书类型': ‘’,
    '原告': ‘’,
    '被告': ‘’,
    '原告律师事务所': ‘’,
    '被告律师事务所': ‘’,
    '案由': ‘’,
    '涉案金额（元）': ‘’,
    '判决结果': ‘’,
    '日期': ‘’,
    '文件名': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    # print(identifier)
    row = legal_document[(legal_document['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_legal_document_company_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【关联公司】查询所有【裁判文书】结构化相关信息
    {
    '关联公司': '',
    '标题': '',
    '案号': '',
    '文书类型': ‘’,
    '原告': ‘’,
    '被告': ‘’,
    '原告律师事务所': ‘’,
    '被告律师事务所': ‘’,
    '案由': ‘’,
    '涉案金额（元）': ‘’,
    '判决结果': ‘’,
    '日期': ‘’,
    '文件名': ‘’}
    :param identifier: 关联公司
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = legal_document[(legal_document['关联公司'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_legal_document_law_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【律师事务所】查询所有【裁判文书】结构化相关信息
    {
    '关联公司': '',
    '标题': '',
    '案号': '',
    '文书类型': ‘’,
    '原告': ‘’,
    '被告': ‘’,
    '原告律师事务所': ‘’,
    '被告律师事务所': ‘’,
    '案由': ‘’,
    '涉案金额（元）': ‘’,
    '判决结果': ‘’,
    '日期': ‘’,
    '文件名': ‘’}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = legal_document[
        (legal_document['原告律师事务所'] == identifier) | (legal_document['被告律师事务所'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_court_info(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【法院名称】查询【法院名录】相关信息
    {
    '法院名称': '',
    '法院负责人': '',
    '成立日期': '',
    '法院地址': ‘’,
    '联系电话': ‘’,
    '法院网站': ‘’}
    :param identifier: 法院名称
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = court_info[(court_info['法院名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_court_info_list(prov: Annotated[str, "The province of the court."], city: Annotated[str, "The city of the court."], county: Annotated[str, "The county of the court."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【省市区】查询所有【法院】相关信息
    {
    '法院名称': '',
    '法院负责人': '',
    '成立日期': '',
    '法院地址': ‘’,
    '联系电话': ‘’,
    '法院网站': ‘’,
    '法院省份': ‘’,
    '法院城市': ‘’,
    '法院区县': ‘’}
    :param identifier: 省市区
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = court_info[
        (court_info['法院省份'] == prov) & (court_info['法院城市'] == city) & (court_info['法院区县'] == county)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_court_code(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【法院名称或者法院代字】查询【法院代字】等相关数据
    {
    '法院名称': '',
    '行政级别': '',
    '法院级别': '',
    '法院代字': '',
    '区划代码': '',
    '级别': ''}
    :param identifier: 法院名称或者法院代字
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = court_code[(court_code['法院名称'] == identifier) |
                     (court_code['法院代字'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_lawfirm_info(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【律师事务所】查询【律师事务所名录】

    {
    '律师事务所名称': '',
    '律师事务所唯一编码': '',
    '律师事务所负责人': '',
    '事务所注册资本': '',
    '事务所成立日期': '',
    '律师事务所地址': '',
    '通讯电话': '',
    '通讯邮箱': '',
    '律所登记机关': ''}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = lawfirm_info[(lawfirm_info['律师事务所名称'] == identifier) |
                       (lawfirm_info['律师事务所唯一编码'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_lawfirm_info_list(prov: Annotated[str, "The province of the lawfirm."], city: Annotated[str, "The city of the lawfirm."], county: Annotated[str, "The county of the lawfirm."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【省市区】查询所有【律所】相关信息
    {
    '律师事务所名称': '',
    '律师事务所唯一编码': '',
    '律师事务所负责人': '',
    '事务所注册资本': '',
    '事务所成立日期': '',
    '律师事务所地址': '',
    '通讯电话': '',
    '通讯邮箱': '',
    '律所登记机关': '',
    '事务所省份': '',
    '事务所城市': '',
    '事务所区县': ''}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = lawfirm_info[(lawfirm_info['事务所省份'] == prov) & (lawfirm_info['事务所城市'] == city) & (
            lawfirm_info['事务所区县'] == county)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_lawfirm_log(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【律师事务所】查询【律师事务所服务记录】
    {
    '律师事务所名称': '',
    '业务量排名': '',
    '服务已上市公司': '',
    '报告期间所服务上市公司违规事件': '',
    '报告期所服务上市公司接受立案调查': ''}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = lawfirm_log[(lawfirm_log['律师事务所名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_address_info(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【公司地址】查询地址所在【省市区】
    {
    '地址': '',
    '省份': '',
    '城市': '',
    '区县': ''}
    :param identifier: 地址
    :param columns: 需要返回的列名列表
    :return: 地址信息字典或错误信息
    '''

    row = address_info[address_info['地址'] == identifier]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_legal_abstract(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【案号】查询【文本摘要】
    {
    '文件名': '',
    '案号': '',
    '文本摘要': ''}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 地址信息字典或错误信息
    '''

    row = legal_abstract[(legal_abstract['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}

@tool
@log_io
@exception_handler
def get_restriction_case(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【案号】查询【限制高消费】相关信息
    {
    '限制高消费企业名称': '',
    '案号': '',
    '法定代表人': ‘’,
    '申请人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '限高发布日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = restriction_case[(restriction_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_restriction_case_company_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【限制高消费企业名称】查询所有【限制高消费】相关信息
    {
    '限制高消费企业名称': '',
    '案号': '',
    '法定代表人': ‘’,
    '申请人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '限高发布日期': ‘’}
    :param identifier: 限制高消费企业名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = restriction_case[(restriction_case['限制高消费企业名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_restriction_case_court_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【法院】查询所有【限制高消费】相关信息
    {
    '限制高消费企业名称': '',
    '案号': '',
    '法定代表人': ‘’,
    '申请人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '限高发布日期': ‘’}
    :param identifier: 限制高消费企业名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = restriction_case[(restriction_case['执行法院'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_finalized_case(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【案号】查询【终本】相关信息
    {
    '终本公司名称': '',
    '案号': '',
    '被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '未履行金额（元）': ‘’,
    '执行标的（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '终本日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = finalized_case[(finalized_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_finalized_case_company_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【企业名称】查询所有【终本】相关信息
    {
    '终本公司名称': '',
    '案号': '',
    '被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '未履行金额（元）': ‘’,
    '执行标的（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '终本日期': ‘’}
    :param identifier: 终本公司名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = finalized_case[(finalized_case['终本公司名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_finalized_case_court_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【法院】查询所有【终本】相关信息
    {
    '终本公司名称': '',
    '案号': '',
    '被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '未履行金额（元）': ‘’,
    '执行标的（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '终本日期': ‘’}
    :param identifier: 法院
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = finalized_case[(finalized_case['执行法院'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_dishonesty_case(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【案号】查询【失信被执行】相关信息
    {
    '失信被执行公司名称': '',
    '案号': '',
    '失信被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '发布日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = dishonesty_case[(dishonesty_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_dishonesty_case_company_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【企业名称】查询所有【失信被执行】相关信息
    {
    '失信被执行公司名称': '',
    '案号': '',
    '失信被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '发布日期': ‘’}
    :param identifier: 失信被执行公司名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = dishonesty_case[(dishonesty_case['失信被执行公司名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


@tool
@log_io
@exception_handler
def get_dishonesty_case_court_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【法院】查询所有【失信被执行】相关信息
    {
    '失信被执行公司名称': '',
    '案号': '',
    '失信被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '发布日期': ‘’}
    :param identifier: 法院
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = dishonesty_case[(dishonesty_case['执行法院'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return {}


@tool
@log_io
@exception_handler
def get_administrative_case(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【案号】查询【行政处罚】相关信息
    {
    '行政处罚公司名称': '',
    '案号': '',
    '事实': ‘’,
    '处罚结果': ‘’,
    '处罚金额（元）': ‘’,
    '处罚单位': ‘’,
    '处罚日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = administrative_case[(administrative_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return {}


@tool
@log_io
@exception_handler
def get_administrative_case_company_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【企业名称】查询所有【行政处罚】相关信息
    {
    '行政处罚公司名称': '',
    '案号': '',
    '事实': ‘’,
    '处罚结果': ‘’,
    '处罚金额（元）': ‘’,
    '处罚单位': ‘’,
    '处罚日期': ‘’}
    :param identifier: 行政处罚公司名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = administrative_case[(administrative_case['行政处罚公司名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return {}


@tool
@log_io
@exception_handler
def get_administrative_case_court_list(identifier: Annotated[str, "The identifier of the company."], columns: Annotated[list[str] | None, "The columns to return."] = None) -> dict | list | str:
    '''
    根据【处罚单位】查询所有【行政处罚】相关信息
    {
    '行政处罚公司名称': '',
    '案号': '',
    '事实': ‘’,
    '处罚结果': ‘’,
    '处罚金额（元）': ‘’,
    '处罚单位': ‘’,
    '处罚日期': ‘’}
    :param identifier: 处罚单位
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = administrative_case[(administrative_case['处罚单位'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return []


key1_not_list = [
    '公司简称', '英文名称', '关联证券', '公司代码', '曾用简称', '所属市场', '所属行业', '成立日期', '上市日期',
    '法人代表', '总经理', '董秘', '邮政编码', '注册地址', '办公地址', '联系电话', '传真', '官方网址', '电子邮箱',
    '入选指数', '主营业务', '经营范围', '机构简介', '每股面值', '首发价格', '首发募资净额', '首发主承销商']
key2_not_list = [
    '登记状态', '统一社会信用代码', '法定代表人', '注册资本', '成立日期', '企业地址', '联系电话', '联系邮箱', '注册号',
    '组织机构代码',
    '参保人数', '行业一级', '行业二级', '行业三级', '曾用名', '企业简介', '经营范围'
]
key3_not_list = ['上市公司关系']
key4_not_list = [
    '关联公司', '标题', '文书类型', '原告', '被告', '原告律师事务所', '被告律师事务所', '案由', '涉案金额（元）',
    '判决结果', '日期', '文件名'
]
key5_not_list = [
    '法院名称', '法院负责人', '成立日期', '法院地址', '联系电话', '法院官网'
]
key6_not_list = ['法院名称', '行政级别', '法院级别', '法院代字', '区划代码']
key7_not_list = [
    '律师事务所唯一编码', '律师事务所负责人', '事务所注册资本', '事务所成立日期', '律师事务所地址',
    '通讯电话', '通讯邮箱', '律所登记机关'
]
key8_not_list = [
    '律师事务所名称', '业务量排名', '服务已上市公司', '报告期间所服务上市公司违规事件', '报告期所服务上市公司接受立案调查'
]
key9_not_list = ['省份', '城市', '区县']
key10_not_list = ['省份', '城市', '区县', '城市区划代码', '区县区划代码']
key11_not_list = ['日期', '省份', '城市', '天气', '最高温度', '最低温度', '湿度']
key12_not_list = ['案号', '文件名', '文本摘要']

all_list = []

# %%
# 1 get_company_info 根据【公司名称、公司简称或公司代码】查找【上市公司】信息 company_info
# 2 get_company_register 根据【公司名称】查询【工商】信息 company_register
# 3 get_company_register_name 根据【统一社会信用代码】查询【公司名称】 company_register
# 4 get_sub_company_info 根据【被投资的公司名称】查询【母公司及投资】信息 sub_company_info
# 5 get_sub_company_info_list 根据【母公司的名称】查询所有【投资的子公司信息】信息 sub_company_info
# 6 get_legal_document 根据【案号】查询【裁判文书】结构化相关信息 legal_document
# 7 get_legal_document_company_list 根据【关联公司】查询所有【裁判文书】结构化相关信息 legal_document
# 8 get_legal_document_law_list 根据【律师事务所】查询所有【裁判文书】结构化相关信息 legal_document
# 9 get_court_info 根据【法院名称】查询【法院名录】相关信息 court_info
# 10 get_court_info_list 根据【省市区】查询所有【法院】相关信息 court_info
# 11 get_court_code 根据【法院名称或者法院代字】查询【法院代字】等相关数据 court_code
# 12 get_lawfirm_info 根据【律师事务所】查询【律师事务所名录】 lawfirm_info
# 13 get_lawfirm_info_list 根据【省市区】查询所有【律所】相关信息 lawfirm_info
# 14 get_lawfirm_log 根据【律师事务所】查询【律师事务所服务记录】 lawfirm_log
# 15 get_address_info 根据【公司地址】查询地址所在【省市区】 address_info
# 16 get_legal_abstract 根据【案号】查询【文本摘要】 legal_abstract
# 17 get_restriction_case 根据【案号】查询【限制高消费】相关信息 restriction_case
# 18 get_restriction_case_company_list 根据【限制高消费企业名称】查询所有【限制高消费】相关信息 restriction_case
# 19 get_restriction_case_court_list 根据【法院】查询所有【限制高消费】相关信息 restriction_case
# 20 get_finalized_case 根据【案号】查询【终本】相关信息 finalized_case
# 21 get_finalized_case_company_list 根据【企业名称】查询所有【终本】相关信息 finalized_case
# 22 get_finalized_case_court_list 根据【法院】查询所有【终本】相关信息 finalized_case
# 23 get_dishonesty_case 根据【案号】查询【失信被执行】相关信息 dishonesty_case
# 24 get_dishonesty_case_company_list 根据【企业名称】查询所有【失信被执行】相关信息 dishonesty_case
# 25 get_dishonesty_case_court_list 根据【法院】查询所有【失信被执行】相关信息 dishonesty_case
# 26 get_administrative_case 根据【案号】查询【行政处罚】相关信息 administrative_case
# 27 get_administrative_case_company_list 根据【企业名称】查询所有【行政处罚】相关信息 administrative_case
# 28 get_administrative_case_court_list 根据【处罚单位】查询所有【行政处罚】相关信息 administrative_case
# 29 get_save_dict_list_to_word 创建一个 Word 文档


# print(get_company_info('金宏气体股份有限公司', ['公司代码', '法人代表', '董秘']))

# print(get_legal_document('（2019）鲁0323民初410号',['涉案金额（元）']))
# res = get_legal_document_law_list('上海柏年律师事务所',['涉案金额（元）', '被告'])
# print(res)

# "answer": "上海柏年律师事务所参与的案件中，被告是上市公司的有利亚德光电股份有限公司、南京我乐家居股份有限公司。",

# res = get_legal_document_law_list('湖北斯洋律师事务所',['涉案金额（元）', '被告'])
# print(res)
# for r in res:
#     print(r)

#     if r['被告'].find(',') != -1:
#         r1, r2 = r['被告'].split(',')
#         print(r1)
#         print(get_company_info(r1))
#         print(r2)
#         print(get_company_info(r2))

#     ans = get_company_info(r['被告'])
#     print(ans)

# print(get_company_info('太和县长青保健品销售有限公司'))
# print(get_company_info('太和县资坊堂生物科技有限公司'))
# print(get_company_register_name('91513231068950977H'))

# print(get_court_info_list("安徽省","池州市","贵池区",['法院名称']))
