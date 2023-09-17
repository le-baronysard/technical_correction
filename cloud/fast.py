import fastapi
import joblib
import pandas as pd

app =  fastapi.FastAPI()

# Putting the model in memory at the start of the app
app.state.pipe = joblib.load("pipe.joblib")

# Define a root `/` endpoint
@app.get("/")
def root(truc=0):
    return {"Hello": "World"}

# First method post and get a json for one line prediction
# Define a predict endpoint with a get method
@app.get("/predict")
def predict( account_amount_added_12_24m,
       account_days_in_dc_12_24m, account_days_in_rem_12_24m,
       account_days_in_term_12_24m, account_incoming_debt_vs_paid_0_24m,
       account_status, account_worst_status_0_3m,
       account_worst_status_12_24m, account_worst_status_3_6m,
       account_worst_status_6_12m, age, avg_payment_span_0_12m,
       avg_payment_span_0_3m, merchant_category, merchant_group,
       has_paid, max_paid_inv_0_12m, max_paid_inv_0_24m, name_in_email,
       num_active_div_by_paid_inv_0_12m, num_active_inv,
       num_arch_dc_0_12m, num_arch_dc_12_24m, num_arch_ok_0_12m,
       num_arch_ok_12_24m, num_arch_rem_0_12m,
       num_arch_written_off_0_12m, num_arch_written_off_12_24m,
       num_unpaid_bills, status_last_archived_0_24m,
       status_2nd_last_archived_0_24m, status_3rd_last_archived_0_24m,
       status_max_archived_0_6_months, status_max_archived_0_12_months,
       status_max_archived_0_24_months, recovery_debt,
       sum_capital_paid_account_0_12m, sum_capital_paid_account_12_24m,
       sum_paid_inv_0_12m, time_hours, worst_status_active_inv, uuid
       ,truc = 0
    ):

    # load the  model
    pipe = joblib.load("pipe.joblib")

    # create a dataframe with the data we want to predict
    data = pd.DataFrame(
         {"account_amount_added_12_24m":[account_amount_added_12_24m]
        ,"account_days_in_dc_12_24m":[account_days_in_dc_12_24m]
       ,"account_days_in_rem_12_24m":[account_days_in_rem_12_24m]
       ,"account_days_in_term_12_24m":[account_days_in_term_12_24m]
       ,"account_incoming_debt_vs_paid_0_24m":[account_incoming_debt_vs_paid_0_24m]
       ,"account_status":[account_status]
       ,"account_worst_status_0_3m":[account_worst_status_0_3m]
       ,"account_worst_status_12_24m":[account_worst_status_12_24m]
       ,"account_worst_status_3_6m":[account_worst_status_3_6m]
       ,"account_worst_status_6_12m":[account_worst_status_6_12m]
       ,"age":[age]
       ,"avg_payment_span_0_12m":[avg_payment_span_0_12m]
       ,"avg_payment_span_0_3m":[avg_payment_span_0_3m]
       ,"merchant_category":[merchant_category]
       ,"merchant_group":[merchant_group]
       ,"has_paid":[has_paid]
       ,"max_paid_inv_0_12m":[max_paid_inv_0_12m]
       ,"max_paid_inv_0_24m":[max_paid_inv_0_24m]
       ,"name_in_email":[name_in_email]
       ,"num_active_div_by_paid_inv_0_12m":[num_active_div_by_paid_inv_0_12m]
       ,"num_active_inv":[num_active_inv]
       ,"num_arch_dc_0_12m":[num_arch_dc_0_12m]
       ,"num_arch_dc_12_24m":[num_arch_dc_12_24m]
       ,"num_arch_ok_0_12m":[num_arch_ok_0_12m]
       ,"num_arch_ok_12_24m":[num_arch_ok_12_24m]
       ,"num_arch_rem_0_12m":[num_arch_rem_0_12m]
       ,"num_arch_written_off_0_12m":[num_arch_written_off_0_12m]
       ,"num_arch_written_off_12_24m":[num_arch_written_off_12_24m]
       ,"num_unpaid_bills":[num_unpaid_bills]
       ,"status_last_archived_0_24m":[status_last_archived_0_24m]
       ,"status_2nd_last_archived_0_24m":[status_2nd_last_archived_0_24m]
       ,"status_3rd_last_archived_0_24m":[status_3rd_last_archived_0_24m]
       ,"status_max_archived_0_6_months":[status_max_archived_0_6_months]
       ,"status_max_archived_0_12_months":[status_max_archived_0_12_months]
       ,"status_max_archived_0_24_months":[status_max_archived_0_24_months]
       ,"recovery_debt":[recovery_debt]
       ,"sum_capital_paid_account_0_12m":[sum_capital_paid_account_0_12m]
       ,"sum_capital_paid_account_12_24m":[sum_capital_paid_account_12_24m]
       ,"sum_paid_inv_0_12m":[sum_paid_inv_0_12m]
       ,"time_hours":[time_hours]
       ,"worst_status_active_inv":[worst_status_active_inv]
       ,"uuid":[uuid]
         }
    )

    # cleaning data the same way we did in the notebook
    data.drop(columns=["worst_status_active_inv"
                   ,"account_worst_status_12_24m"
                   ,"account_worst_status_6_12m"
                   ,"account_incoming_debt_vs_paid_0_24m"
                   ,"account_worst_status_3_6m"
                   ,"account_status"
                   ,"account_worst_status_0_3m"
                   ,"avg_payment_span_0_3m"
                   ]
              ,inplace=True)


    # using the pipeline to preprocess & predict
    prediction =  int(pipe.predict(data)[0]) # we want an int not a np.int64

    return prediction


# Second method post and get a csv for multilines predictions

from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse # Add to Top

# File read as UploadFile (it is already a file-like object)
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}

    try :
        data = pd.read_csv(file.file,delimiter=";")
        # Might be better to tcheck the columns names

    except:
        return {"message": "Not a csv file or Incorrect delimiter expected ';'"}

        # cleaning data the same way we did in the notebook
    data.drop(columns=["worst_status_active_inv"
                   ,"account_worst_status_12_24m"
                   ,"account_worst_status_6_12m"
                   ,"account_incoming_debt_vs_paid_0_24m"
                   ,"account_worst_status_3_6m"
                   ,"account_status"
                   ,"account_worst_status_0_3m"
                   ,"avg_payment_span_0_3m"
                   ]
              ,inplace=True)


    # using the pipeline to preprocess & predict
    prediction =  pd.DataFrame({ "uuid":data["uuid"]
                                ,"prediction":app.state.pipe.predict(data)
                                })

    # return the prediction as a csv file
    return StreamingResponse(
                            iter([prediction.to_csv(index=False)]),
                            media_type="text/csv",
                            headers={"Content-Disposition": f"attachment; filename=data.csv"}
                    )


# To go further : https://fastapi.tiangolo.com/tutorial/request-files/
# The other possibilite for a post file is to read the file as a binary
# File read as binary
@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No csv sent"}
    else:
        return {"file_size": len(file)}
