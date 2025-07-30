# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

from langchain_core.tools import tool
from src.tools.law.api import *

def get_lawyer_tools():
    # 返回`api.py`中的除了`load_data_with_cache`的所有函数，如[get_company_info]
    return [get_company_info, get_company_register, get_sub_company_info, get_sub_company_info_list, get_legal_document, get_legal_document_company_list, get_legal_document_law_list, get_court_info, get_court_info_list, get_court_code, get_lawfirm_info, get_lawfirm_info_list, get_lawfirm_log, get_address_info, get_legal_abstract, get_restriction_case, get_restriction_case_company_list, get_restriction_case_court_list, get_finalized_case, get_finalized_case_company_list, get_finalized_case_court_list, get_dishonesty_case, get_dishonesty_case_company_list, get_dishonesty_case_court_list, get_administrative_case, get_administrative_case_company_list, get_administrative_case_court_list]

if __name__ == "__main__":
    print(get_lawyer_tools())
    print(len(get_lawyer_tools())) # 27