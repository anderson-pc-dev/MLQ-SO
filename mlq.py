from typing import List
from Core.Process import Process
from Core.MLQQueue import MLQQueue
from Core.ProcessFileManager import ProcessFileManager

class MLQ:
    """
    Clase principal que implementa el algoritmo Multi-Level Queue (MLQ) para la planificación de procesos.

    Esta clase organiza y gestiona tres colas de planificación con políticas diferentes:
    - Round Robin con quantum 1 (RR1)
    - Round Robin con quantum 3 (RR3)
    - Shortest Job First (SJF)

    También rastrea el tiempo actual del sistema y los procesos que están en ejecución o han sido completados.

    Atributos:
    ----------
    queues : List[MLQQueue]
        Lista de colas, donde cada cola sigue una política de planificación diferente:
        - "RR1": Planificación Round Robin con quantum 1.
        - "RR3": Planificación Round Robin con quantum 3.
        - "SJF": Planificación Shortest Job First (sin quantum).
    
    current_time : int
        El tiempo actual del sistema, que avanza conforme los procesos se ejecutan. Inicialmente es 0.
    
    processes : List[Process]
        Lista de todos los procesos cargados en el sistema que están en alguna de las colas y esperando ser ejecutados.
    
    completed_processes : List[Process]
        Lista de procesos que ya han sido ejecutados y completados. Cada proceso en esta lista tiene sus métricas (como tiempo de finalización, tiempo de espera, etc.) calculadas.
    """
    def __init__(self):
        self.queues = [
            MLQQueue("RR1", 1),
            MLQQueue("RR3", 3),
            MLQQueue("SJF")
        ]
        self.current_time = 0
        self.processes: List[Process] = []
        self.completed_processes: List[Process] = []


    def load_processes(self, filename: str):
        """
        Utiliza ProcessFileManager para cargar los procesos desde un archivo.
        """
        self.processes = ProcessFileManager.load_processes_from_file(filename)


    def add_process(self, process: Process):
        """
        Añade un proceso a su cola correspondiente en función de su atributo `queue`.

        Cada proceso tiene un atributo `queue` que indica a cuál de las tres colas (RR1, RR3 o SJF) debe ser asignado.
        El índice de la cola se obtiene restando 1 del valor de `queue`, ya que las colas están organizadas en una lista.

        Parámetros:
        -----------
        process : Process
            El proceso que se va a añadir a la cola correspondiente según su atributo `queue`.
        """
        # Restar 1 al número de cola porque las colas están en una lista (0 = RR1, 1 = RR3, 2 = SJF)
        self.queues[process.queue - 1].add_process(process)

    def run(self):
        """
        Ejecuta el algoritmo Multi-Level Queue (MLQ) gestionando los procesos según las colas y sus políticas de planificación.

        Este método controla el ciclo de ejecución de los procesos, despachándolos de las colas en el orden adecuado,
        respetando las prioridades y las políticas de planificación de cada cola (RR con quantum y SJF).
        El ciclo se ejecuta mientras haya procesos pendientes o procesos en las colas.

        """

        # Ordenar los procesos por su tiempo de llegada
        self.processes.sort(key=lambda p: p.arrival_time)
        
        while self.processes or any(not q.is_empty() for q in self.queues):
            # Añadir procesos que han llegado a las colas correspondientes
            while self.processes and self.processes[0].arrival_time <= self.current_time:
                self.add_process(self.processes.pop(0))

            executed = False
            # Iterar sobre las colas y ejecutar procesos
            for queue in self.queues:
                if not queue.is_empty():
                    # Obtener el siguiente proceso de la cola
                    process = queue.get_process()

                    # Si es la primera vez que el proceso se ejecuta, calcular su response_time
                    if process.first_run_time is None:
                        process.first_run_time = self.current_time
                        process.response_time = process.first_run_time - process.arrival_time

                    # Determinar el tiempo de ejecución según el quantum (si aplica) o ejecutar completamente (SJF)
                    if queue.quantum:  # Para colas RR (Round Robin)
                        execution_time = min(queue.quantum, process.remaining_time)
                    else:  # Para la cola SJF (Shortest Job First)
                        execution_time = process.remaining_time

                    # Avanzar el tiempo actual y reducir el tiempo restante del proceso
                    self.current_time += execution_time
                    process.remaining_time -= execution_time

                    # Si el proceso ha terminado
                    if process.remaining_time == 0:
                        process.completion_time = self.current_time
                        process.turnaround_time = process.completion_time - process.arrival_time
                        process.waiting_time = process.turnaround_time - process.burst_time
                        self.completed_processes.append(process)
                        print(f"Proceso {process.id} completado en tiempo {self.current_time}")
                    else:
                        # Si no ha terminado, reinsertarlo en la cola
                        process.last_execution_time = self.current_time
                        queue.add_process(process)
                        print(f"Proceso {process.id} ejecutado por {queue.name} hasta tiempo {self.current_time}")

                    executed = True
                    # Después de ejecutar un proceso, volver a verificar las colas de mayor prioridad
                    break

            if not executed:
                # Si no se ejecutó ningún proceso, avanzar el tiempo hasta el próximo proceso que llegue
                if self.processes:
                    # Mover el tiempo actual al tiempo de llegada del siguiente proceso
                    self.current_time = max(self.current_time, self.processes[0].arrival_time)
                else:
                    # Encontrar el tiempo más cercano de un proceso en las colas
                    next_process_time = min(
                        (q.processes.queue[0].arrival_time for q in self.queues if not q.is_empty()),
                        default=self.current_time
                    )
                    self.current_time = max(self.current_time, next_process_time)

    def write_results(self, output_filename: str):
        """
        Utiliza ProcessFileManager para escribir los resultados en un archivo.
        """
        ProcessFileManager.write_process_results_to_file(self.completed_processes, output_filename)
                    
# Ejemplo de uso
if __name__ == "__main__":
    nombre = "mlq001"
    mlq = MLQ()
    mlq.load_processes(nombre+".txt")
    mlq.run()
    mlq.write_results(nombre+"_output.txt")