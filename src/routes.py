from flask import Flask, render_template
from getJobHistory import getStats, getItemList


app = Flask(__name__)

@app.route('/')
def main_page():
    stats = getStats(getItemList())

    return render_template('statTemplate.html', totalItems = stats['totalItems'], 
                            avgFilesPerDay = stats['avgFilesPerDay'], totalUploadBytes = stats['totalUploadBytes'], 
                            totalCompressedBytes = stats['totalCompressedBytes'], totalBytesSaved = stats['totalBytesSaved'],
                            percentBytesSaved = stats['percentBytesSaved'])