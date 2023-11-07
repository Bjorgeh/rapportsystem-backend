#Get request for testing API connection

'''
@ns.route('/test')
class Test(Resource):
    @api.doc('get_test')
    
    #requires valid session
    @require_session

    def get(self):
        #returns test data
        return {"Test": "OK", "Session": logged_in_user.getSessionID()}, 200
'''