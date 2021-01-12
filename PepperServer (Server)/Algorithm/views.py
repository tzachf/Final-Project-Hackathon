from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from Stroke_code import feature_Selection as mlAlgorithm
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def analyzeMovement(request):
    analyze_csv = request.FILES['file']
    directory = analyze_csv.name
    project_root = "./compensation_detection/Data/Soroka"
    mode = 0o666
    input_path = os.path.join(project_root, directory)
    os.makedirs(input_path, mode)
    input_pathCSV = input_path + "\\" + directory
    path = default_storage.save(input_pathCSV, ContentFile(analyze_csv.read()))
    tmp_file = os.path.join(directory, path)

    # init data
    LABEL = 'PatientID'
    TASK = 'taskID'
    DATA_PATH = './compensation_detection/Data/Soroka'
    DATA_KIND = 'train'
    features = ['wrist_X', 'wrist_Y', 'wrist_Z', 'shoulder_X', 'shoulder_Z', 'elbow_X']
    output_fold = 'code_products'

    # create train
    X_train, Y_train = mlAlgorithm.read_tsfresh_data(
        x_path=f'{DATA_PATH}/{output_fold}/tsfresh_features_{DATA_KIND}.csv',
        y_path=f'{DATA_PATH}/{output_fold}/patients_labels.csv')

    input_fold = 'organized_test_data'
    DATA_KIND = 'test'
    mlAlgorithm.create_tsfresh_data(features, input_fold, output_fold, LABEL, TASK, data_kind=DATA_KIND)
    X_test, Y_test = mlAlgorithm.read_tsfresh_data(
        x_path=f'{DATA_PATH}\\{output_fold}\\tsfresh_features_{DATA_KIND}.csv',
        y_path=f'{DATA_PATH}\\{output_fold}\\patients_labels_test.csv', merge='inner')
    print("im here")
    ans = mlAlgorithm.run_rakel_full(X_train.values, Y_train.values, X_test.values, Y_test.values)
    print(ans)
    # compensation_detection = mlAlgorithm.predict_compensation(input_path)
    # SIMULATE COMPENSATION DETECTION ALGORITHM
    # trunk_flex = randint(0, 1)
    # scapular_e = randint(0, 1)
    # scapular_r = randint(0, 1)
    # shoulder_flex = randint(0, 1)
    # elbow_flex = randint(0, 1)
    # distal_dys_syn = randint(0, 1)
    #
    # compensation_detection = [
    #     ["trunk-flex", "scapular-e", "scapular-r", "shoulder-flex", "elbow-flex", "distal-dys-syn"],
    #     [trunk_flex, scapular_e, scapular_r, shoulder_flex, elbow_flex, distal_dys_syn]]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="compensations.csv"'

    # writer = csv.writer(response)
    # writer.writerows(compensation_detection)

    return response

# Create your views here.