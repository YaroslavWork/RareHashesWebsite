from flask import Blueprint, render_template, redirect, request, url_for, current_app

from app.database_utils.hash_database_utils import get_hashes_in_ranges, count_all_hashes

view_bp = Blueprint("view", __name__)


@view_bp.route('/view', methods=["GET"])
def view():
    """View route [/view -> /view/1?createdAt=-1]: A list of hashes (redirect if just default values)"""

    return redirect(url_for('view.view_with_params', page=1, createdAt=-1))


@view_bp.route('/view/<int:page>')
def view_with_params(page: int):
    """View route (with parameters) [/view/<int:page>?<parameters>]: A list of hashes"""

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

    result = get_hashes_in_ranges(database, row_in_one_page_limit*(page-1), row_in_one_page_limit, sort_data)
    count = count_all_hashes(database)

    return render_template('view.html', result=result, count=count, start_count=int((page-1)*row_in_one_page_limit)+1)