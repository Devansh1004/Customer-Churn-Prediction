from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Literal
from datetime import datetime

class Request(BaseModel):
    # TODO add descriptions
    
    Customer_Age : Annotated[
        int, 
        Field(ge=18, le=120)
    ]
    
    Gender : Annotated[
        Literal['M', 'F'], 
        Field()
    ]
    
    Dependent_count : Annotated[
        int, 
        Field(ge=0, le=5)
    ]
    
    Education_Level : Annotated[
        Literal['Uneducated', 'High School', 'College', 'Graduate', 'Post-Graduate', 'Doctorate','Unknown'], 
        Field()
    ]
    
    Marital_Status : Annotated[
        Literal['Single', 'Married', 'Divorced', 'Unknown'],
        Field()
    ]
    
    Income_Category : Annotated[
        Literal['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +', 'Unknown'],
        Field()
    ]
    
    Card_Category : Annotated[
        Literal['Blue', 'Silver', 'Gold', 'Platinum'],
        Field()
    ]
    
    Months_on_book : Annotated[
        int, 
        Field(ge=0, le=60)
    ]
    
    Total_Relationship_Count : Annotated[
        int, 
        Field(ge=1)
    ]
    
    Months_Inactive_12_mon : Annotated[
        int, 
        Field(ge=0, le=12)
    ]
    
    Contacts_Count_12_mon : Annotated[
        int, 
        Field(ge=0)
    ]

    Credit_Limit : Annotated[
        float, 
        Field(ge=0, le=40000)
    ]
    
    Total_Revolving_Bal : Annotated[
        float, 
        Field(ge=0, le=4000)
    ]
    
    Avg_Open_To_Buy : Annotated[
        float,
        Field(ge=0, le=40000)
    ]
    
    Total_Amt_Chng_Q4_Q1 : Annotated[
        float,
        Field(ge=0, le=5)
    ]
    
    Total_Trans_Amt : Annotated[
        float,
        Field(ge=0, le=20000)
    ]
    
    Total_Trans_Ct : Annotated[
        float,
        Field(ge=0, le=150)
    ]
    
    Total_Ct_Chng_Q4_Q1 : Annotated[
        float,
        Field(ge=0, le=5)
    ]
    
    Avg_Utilization_Ratio : Annotated[
        float,
        Field(ge=0, le=1)
    ]
    
class Response(BaseModel):
    prediction : Annotated[
        Literal[0, 1],
        Field()
    ]
    
    churn_probability : Annotated[
        float,
        Field(ge=0, le=1)
    ]
    
    display_probability : Annotated[
        float,
        Field(ge=0, le=1)
    ] 
    
class DBResponse(BaseModel):
    
    id : Annotated[
        int,
        Field()
    ]
    
    timestamp : Annotated[
        datetime,
        Field()
    ]
    
    prediction : Annotated[
            Literal[0, 1],
            Field()
        ]
        
    churn_probability : Annotated[
        float,
        Field(ge=0, le=1)
    ]
    
    display_probability : Annotated[
        float,
        Field(ge=0, le=1)
    ]
    
    model_version : Annotated[
        str,
        Field(max_length=20)
    ]
    
    model_config = ConfigDict(
        from_attributes = True
    )
    
class PredictionStatsresponse(BaseModel):
    total_predictions : int
    churn_predictions : int
    non_churn_predictions : int
    mean_churn_probability : float
    