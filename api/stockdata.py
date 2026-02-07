from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

app = FastAPI()

# 允许跨域请求（重要，这样你的前端页面才能调用这个API）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stockdata")
async def get_stock_data(days: int = Query(30, ge=1, le=365, description="获取最近N天的数据")):
    try:
        # 1. 获取沪深300指数数据 (价格和PE)
        index_data = ak.index_value_hist_funddb(symbol="沪深300")
        # 确保日期格式正确并排序
        index_data['日期'] = pd.to_datetime(index_data['日期'])
        index_data = index_data.sort_values('日期').tail(days)

        # 2. 获取10年期国债收益率数据
        bond_yield_df = ak.bond_china_yield()
        # 筛选10年期国债，并处理日期
        bond_10y = bond_yield_df[bond_yield_df['期限'] == '10年'].copy()
        bond_10y['日期'] = pd.to_datetime(bond_10y['日期'])
        bond_10y = bond_10y.sort_values('日期').tail(days)

        # 3. 合并数据（以日期为键）
        merged_df = pd.merge(
            index_data[['日期', '收盘', '市盈率']],
            bond_10y[['日期', '收益率']],
            on='日期',
            how='inner'  # 只保留两个数据源都有的日期
        )

        # 4. 格式化为列表字典，便于前端使用
        result = merged_df.to_dict(orient='records')

        return JSONResponse({
            "code": 200,
            "data": result,
            "message": "success"
        })

    except Exception as e:
        return JSONResponse({
            "code": 500,
            "data": None,
            "message": f"数据获取失败: {str(e)}"
        }, status_code=500)

# 用于Vercel Serverless的函数入口
handler = app
