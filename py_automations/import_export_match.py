from ntpath import join
from data_modules import file_handler, data_organizer, vca_handler
import Production_Details 




if __name__ == '__main__':
    import_path = r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\SupportFunctions'
    file = r'meta_filter.csv'


    export_path = [r'C:\LMS\HOST_EXPORT\VCA\read_app',r'Z:\Backup LMS\LMS Export\Backup\2022']


    export_file_list = []
    for path in export_path:
        export_file_list = export_file_list + file_handler.listFilesInDirSubDir(path, 'vca')


    import_file = file_handler.CSVtoList(join(import_path, file), delimeter_char=',')


    import_export_list = []
    import_export_merge = {}
    for job in import_file:
        import_export_merge.update(job)
        file_found = file_handler.file_finder(export_file_list, job['JOB'], 0, 12)
        if file_found:
            vca_converted = vca_handler.VCAtoDict(file_handler.file_reader(file_found))
            filtered_tags_job = data_organizer.filter_tag(vca_converted, 'JOB', 'LDNAM')
            import_export_merge.update(data_organizer.tags_dict_to_plain_dict(filtered_tags_job))
        import_export_list.append(import_export_merge)
        import_export_merge = {}


    file_handler.listToCSV(import_export_list, r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\SupportFunctions\import_export_merge.csv')
