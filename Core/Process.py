from typing import List, Optional


class Process:
    """
    Clase que representa un proceso en el sistema de planificación MLQ (Multi-Level Queue).
    
    Atributos:
    ----------
    id : str
        Identificador único del proceso.
    
    burst_time : int
        Tiempo de CPU requerido por el proceso para completar su ejecución.
        
    arrival_time : int
        Tiempo en el que el proceso llega al sistema (para ser insertado en la cola de listos).
        
    queue : int
        Número de la cola a la que pertenece el proceso. Esto indica la política de planificación que se aplicará (RR1, RR3, SJF).
        
    priority : int
        Prioridad del proceso. Los valores más altos representan una mayor prioridad.
    
    remaining_time : int
        Tiempo restante de CPU que necesita el proceso. Se inicializa con el valor de burst_time y se actualiza conforme avanza la ejecución del proceso.
        
    completion_time : Optional[int]
        Tiempo en el que el proceso completa su ejecución. Se asigna cuando el proceso termina de ejecutarse.
        
    waiting_time : Optional[int]
        Tiempo que el proceso espera en la cola antes de ser ejecutado. Es calculado posteriormente cuando el proceso finaliza.
        
    response_time : Optional[int]
        Tiempo desde que el proceso llega al sistema (arrival_time) hasta que es ejecutado por primera vez. Similar a waiting_time, pero se calcula en el momento en que el proceso comienza su ejecución inicial.
        
    turnaround_time : Optional[int]
        Tiempo total que el proceso pasa en el sistema, desde su llegada hasta su finalización. Se calcula como completion_time - arrival_time.
        
    first_run_time : Optional[int]
        Momento en el que el proceso se ejecuta por primera vez. Esto es útil para calcular el response_time.
        
    last_execution_time : int
        Momento en el que el proceso fue ejecutado por última vez. Se usa para gestionar el orden en las colas de prioridad.

    """    

    def __init__(self, id: str, burst_time: int, arrival_time: int, queue: int, priority: int):
        self.id = id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.queue = queue
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time: Optional[int] = None
        self.waiting_time: Optional[int] = None
        self.response_time: Optional[int] = None
        self.turnaround_time: Optional[int] = None
        self.first_run_time: Optional[int] = None
        self.last_execution_time: int = 0

    def __lt__(self, other):
        """
        Sobrecarga del operador < para la comparación de procesos en colas de prioridad.
        
        Los procesos se ordenan según su prioridad. Un valor de prioridad más alto significa
        mayor prioridad. Si dos procesos tienen la misma prioridad, se puede definir un criterio 
        secundario, pero aquí solo se compara la prioridad.
        
        Parámetros:
        -----------
        other : Process
            El otro proceso con el que se compara este proceso.
        
        Retorna:
        --------
        bool:
            True si este proceso tiene mayor prioridad que 'other', False de lo contrario.
        """
        return self.priority > other.priority

    