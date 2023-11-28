import json
import os
import sys
import time
import glob
from datetime import datetime, timedelta

def support(pin):
    try:
        if pin:
            print(f"Collecting Data for case {pin}...")
            
        else:
            print("Please Provide a PIN-Code")
                    
    except Exception as e:
        handle_exception(f"Error in Support Module: {e}")
        
def handle_exception(error_message):
    print(error_message)