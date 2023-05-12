import datetime
import json
import os
import traceback

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, Header, File
from fastapi.responses import FileResponse, StreamingResponse
from starlette.responses import Response, JSONResponse

from src.scrape.indeed_scraper import IndeedScraper
from src.scrape.scrape_helper import ScrapeHelper
from src.scrape.scrape_request import ScrapeRequest

from src.webapi.job_item_data import JobItemData
from src.webapi.job_logs_data import JobLogsData

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CUR_FILE = os.path.basename(__file__)
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

api_router = APIRouter()

@api_router.get("/")
def health() -> Response:
    return "Healthy"


@api_router.post("/searchjobs")
async def search_job(input_request : Request, background_tasks: BackgroundTasks) -> JSONResponse:
    try:
        input_request_json = await input_request.json()
        location = input_request_json["location"]

        what_job = 'Senior Software Engineer'
        last_days = 14
        max_page = 10

        job_request = ScrapeRequest(location, what_job, last_days, max_page, TODAY)

        background_tasks.add_task(IndeedScraper.run_job, job_request)

        return JSONResponse("job submitted. please check back.", status_code=200)

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            content=f"Error: {ex}\nStackTrace: {traceback.format_exc()}"
        )


@api_router.get("/getjobs")
async def get_jobs(location: str = "") -> JSONResponse:
    try:
        print(f"location = {location}")  # should have been url-decoded

        scraped_jobs = ScrapeHelper.read_job_list(location, TODAY)

        job_list = []
        for idx, item in enumerate(scraped_jobs):
            job_item = JobItemData(
                idx,
                item["JobTitle"],
                item["CompanyName"],
                item["CompanyLocation"],
                item["JobType"],
                item["SalaryInfo"],
                item["JobDescription"],
                item['PostDate'],
                item["ApplyLink"]
            )
            job_list.append(job_item.to_json())

        print(f"joblist = {len(job_list)}")

        return JSONResponse(job_list, status_code=200)
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            content=f"Error: {ex}\nStackTrace: {traceback.format_exc()}"
        )


@api_router.get("/getlogs")
async def get_logs(location: str = "") -> JSONResponse:
    try:
        print(f"location = {location}")

        job_logs = ScrapeHelper.read_job_logs(location, TODAY)

        print(f"job_logs = {len(job_logs)}")

        return JSONResponse(job_logs, status_code=200)

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            content=f"Error: {ex}\nStackTrace: {traceback.format_exc()}"
        )
