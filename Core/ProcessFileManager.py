from typing import List
from Core.Process import Process

class ProcessFileManager:
    """
    Clase encargada de gestionar la carga y escritura de procesos desde y hacia archivos.
    Separa la responsabilidad de entrada/salida de la lógica principal de planificación de procesos.
    """
    
    @staticmethod
    def load_processes_from_file(filename: str) -> List[Process]:
        """
        Carga los procesos desde un archivo dado y los retorna como una lista de instancias de Process.

        Parámetros:
        - `filename` (str): El nombre del archivo desde el cual se cargarán los procesos.

        Retorno:
        - `List[Process]`: Lista de objetos `Process` cargados desde el archivo.
        """
        processes = []
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('#') or line.strip() == '':
                    continue
                parts = line.strip().split(';')
                if len(parts) == 5:
                    id, bt, at, q, priority = parts
                    process = Process(
                        id=id.strip(),
                        burst_time=int(bt.strip()),
                        arrival_time=int(at.strip()),
                        queue=int(q.strip()),
                        priority=int(priority.strip())
                    )
                    processes.append(process)
        return processes

    @staticmethod
    def write_process_results_to_file(processes: List[Process], output_filename: str):
        """
        Escribe los resultados de los procesos completados en un archivo especificado.

        Parámetros:
        - `processes` (List[Process]): Lista de procesos completados con sus métricas calculadas.
        - `output_filename` (str): El nombre del archivo donde se guardarán los resultados.
        """
        with open(output_filename, 'w') as file:
            file.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")
            total_wt, total_ct, total_rt, total_tat = 0, 0, 0, 0
            for process in sorted(processes, key=lambda p: p.id):
                file.write(f"{process.id};{process.burst_time};{process.arrival_time};{process.queue};"
                           f"{process.priority};{process.waiting_time};{process.completion_time};"
                           f"{process.response_time};{process.turnaround_time}\n")
                total_wt += process.waiting_time
                total_ct += process.completion_time
                total_rt += process.response_time
                total_tat += process.turnaround_time

            n = len(processes)
            avg_wt = total_wt / n
            avg_ct = total_ct / n
            avg_rt = total_rt / n
            avg_tat = total_tat / n
            file.write(f"WT={avg_wt:.1f}; CT={avg_ct:.1f}; RT={avg_rt:.1f}; TAT={avg_tat:.1f}\n")