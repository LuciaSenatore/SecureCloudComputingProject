import kfp
from kfp import dsl


@dsl.pipeline(name='First Pipeline', description='Applies Decision Tree and Logistic Regression for a '
                                                 'classification problem.')
def first_pipeline():
    # Loads the yaml manifest for each component
    load_raw_data = kfp.components.load_component_from_file('./data_preprocessing/load_raw_dataset/load_raw_dataset.yaml')
    url_count_digits_ext = kfp.components.load_component_from_file('./data_preprocessing/url_count_digit_ext/url_count_digit_ext.yaml')
    url_count_letters_ext = kfp.components.load_component_from_file('./data_preprocessing/url_count_letters_ext/url_count_letters_ext.yaml')
    url_hasipaddr_ext = kfp.components.load_component_from_file('./data_preprocessing/url_hasipaddr_ext/url_hasipaddr_ext.yaml')
    url_hostname_ext = kfp.components.load_component_from_file('./data_preprocessing/url_hostname_ext/url_hostname_ext.yaml')
    url_https_ext = kfp.components.load_component_from_file('./data_preprocessing/url_https_ext/url_https_ext.yaml')
    url_len_ext = kfp.components.load_component_from_file('./data_preprocessing/url_len_ext/url_len_ext.yaml')
    url_shortserv_ext = kfp.components.load_component_from_file('./data_preprocessing/url_shortserv_ext/url_shortserv_ext.yaml')
    url_spechar_ext = kfp.components.load_component_from_file('./data_preprocessing/url_spechar_ext/url_spechar_ext.yaml')
    load = kfp.components.load_component_from_file('load_data/load_data.yaml')
    decision_tree = kfp.components.load_component_from_file('decision_tree/decision_tree.yaml')
    logistic_regression = kfp.components.load_component_from_file('logistic_regression/logistic_regression.yaml')
    test_decision_tree = kfp.components.load_component_from_file('test_decision_tree/test_decision_tree.yaml')
    test_logistic_regression = kfp.components.load_component_from_file('test_log_regr/test_log_regr.yaml')
    show_result = kfp.components.load_component_from_file('show_result/show_result.yaml')

    # Run load_data task
    load_raw_data_task = load_raw_data()
    url_count_digits_ext_task = url_count_digits_ext(load_raw_data_task.output)
    url_count_letters_ext_task = url_count_letters_ext(load_raw_data_task.output)
    url_hasipaddr_ext_task = url_hasipaddr_ext(load_raw_data_task.output)
    url_hostname_ext_task = url_hostname_ext(load_raw_data_task.output)
    url_https_ext_task = url_https_ext(load_raw_data_task.output)
    url_len_ext_task = url_len_ext(load_raw_data_task.output)
    url_shortserv_ext_task = url_shortserv_ext(load_raw_data_task.output)
    url_spechar_ext_task = url_spechar_ext(load_raw_data_task.output)

    load_task = load(url_count_digits_ext_task.output,url_spechar_ext_task.output,
                     url_hasipaddr_ext_task.output,url_shortserv_ext_task.output,url_count_letters_ext_task.output,
                     url_hostname_ext_task.output,url_https_ext_task.output,url_len_ext_task.output)
    decision_tree_task = decision_tree(load_task.output)
    logistic_regression_task = logistic_regression(load_task.output)
    test_decision_tree_task = test_decision_tree(decision_tree_task.outputs['TestData'], decision_tree_task.outputs['model'],
                                                 decision_tree_task.outputs['scaler'])
    test_logistic_regression_task = test_logistic_regression(logistic_regression_task.outputs['TestData'],logistic_regression_task.outputs['model'],
                                                             logistic_regression_task.outputs['scaler'])
    show_result_task = show_result(test_decision_tree_task.outputs['ModelDT'],
                                   test_decision_tree_task.outputs['ScalerDT'],
                                   test_decision_tree_task.outputs['AccuracyDT'],
                                   test_logistic_regression_task.outputs['ModelLR'],
                                   test_logistic_regression_task.outputs['ScalerLR'],
                                   test_logistic_regression_task.outputs['AccuracyLR'])


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(first_pipeline, 'url_prediction_pipeline.yaml')
