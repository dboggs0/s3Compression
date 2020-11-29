from flask import Flask, render_template
from getJobHistory import getStats, getItemList
app = Flask(__name__)

@app.route('/')
def hello_world():
    stats = getStats(getItemList())
    #{'totalItems': 3, 
    # 'avgFilesPerDay': 3.0,
    # '': Decimal('924642'), 
    # '': Decimal('9276'), 
    # '': Decimal('915366'),
    # '': Decimal('0.9899680092403330153724360347')}
    return render_template('statTemplate.html', totalItems = stats['totalItems'], 
                            avgFilesPerDay = stats['avgFilesPerDay'], totalUploadBytes = stats['totalUploadBytes'], 
                            totalCompressedBytes = stats['totalCompressedBytes'], totalBytesSaved = stats['totalBytesSaved'],
                            percentBytesSaved = stats['percentBytesSaved'])