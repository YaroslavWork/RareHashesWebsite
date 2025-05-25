from flask import Blueprint, render_template, redirect, request, url_for, current_app

from app.database_utils.hash_database_utils import get_hashes_in_ranges

view_bp = Blueprint("view", __name__)

@view_bp.route('/view')
def view():
    return redirect(url_for('view.view_with_params', page=1, createdAt=-1))

@view_bp.route('/view/<int:page>')
def view_with_params(page: int):
    row_in_one_page_limit = current_app.config['ROW_IN_ONE_PAGE_LIMIT']
    database = current_app.config['DATABASE']

    sort_data = []
    sort_args = ['word', 'isFromBeginning', 'counts', 'hashType', 'user', 'createdAt']
    
    for arg in sort_args:
        temp = request.args.get(arg, '0')
        if temp == '1':
            sort_data.append((arg, 1))
        elif temp == '-1':
            sort_data.append((arg, -1))

    if sort_data:
        result = get_hashes_in_ranges(database, row_in_one_page_limit*(page-1), row_in_one_page_limit, sort_data)
    count = database.count()

    return render_template('view.html', result=result, count=count, start_count=int((page-1)*row_in_one_page_limit)+1)