import win32serviceutil
import win32service
import win32event
import servicemanager
import psutil
import time
import json
import datetime
import os

class LolTimeTrackerService(win32serviceutil.ServiceFramework):
    """
    SERVICIO DE WINDOWS PARA MONITOREAR TIEMPO EN LEAGUE OF LEGENDS
    Este servicio se ejecuta en segundo plano y detecta cuando LOL está abierto
    """
    
    # Configuración del servicio Windows
    _svc_name_ = "LolTimeTracker"
    _svc_display_name_ = "Monitor de Tiempo LOL"
    _svc_description_ = "Monitorea el tiempo de juego en League of Legends"

    def __init__(self, args):
        """Inicializar el servicio"""
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        
        # Rutas de archivos
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.script_dir, "lol_time_data.json")
        self.reporte_file = os.path.join(self.script_dir, "reporte_lol.txt")
        
        self.current_session_start = None
        self.load_data()

    def load_data(self):
        """Cargar datos existentes o crear nuevos si no existen"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                
                # Verificar si es un nuevo día para resetear el contador
                ultima_fecha = self.data['ultima_actualizacion'].split('T')[0]
                fecha_actual = datetime.datetime.now().date().isoformat()
                
                if ultima_fecha != fecha_actual:
                    self.data['tiempo_hoy'] = 0
                    self.data['ultima_actualizacion'] = datetime.datetime.now().isoformat()
            else:
                # Datos iniciales si el archivo no existe
                self.data = {
                    'tiempo_hoy': 0,
                    'ultima_actualizacion': datetime.datetime.now().isoformat(),
                    'historial': {}
                }
                
        except Exception as e:
            # Si hay error, crear datos desde cero
            self.data = {
                'tiempo_hoy': 0,
                'ultima_actualizacion': datetime.datetime.now().isoformat(),
                'historial': {}
            }

    def save_data(self):
        """Guardar datos y generar reporte en español"""
        try:
            # Actualizar historial con la fecha actual
            fecha_actual = datetime.datetime.now().date().isoformat()
            self.data['historial'][fecha_actual] = self.data['tiempo_hoy']
            
            # Mantener solo último mes de historial
            un_mes_atras = (datetime.datetime.now() - datetime.timedelta(days=30)).date()
            self.data['historial'] = {
                fecha: tiempo for fecha, tiempo in self.data['historial'].items()
                if datetime.datetime.fromisoformat(fecha).date() >= un_mes_atras
            }
            
            # Guardar datos técnicos en JSON
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            
            # Generar reporte legible en español
            self.generar_reporte_espanol()
                
        except Exception as e:
            # Si falla el guardado, continuar sin interrumpir el servicio
            pass

    def generar_reporte_espanol(self):
        """Generar reporte en formato texto para el usuario"""
        try:
            horas_hoy = self.data['tiempo_hoy'] / 3600
            minutos_hoy = (self.data['tiempo_hoy'] % 3600) / 60
            
            # Calcular total semanal
            ultimos_7_dias = list(self.data['historial'].values())[-7:]
            total_semanal = sum(ultimos_7_dias)
            horas_semanal = total_semanal / 3600
            
            with open(self.reporte_file, 'w', encoding='utf-8') as f:
                f.write("📊 REPORTE DE TIEMPO - LEAGUE OF LEGENDS\n")
                f.write("=" * 50 + "\n")
                f.write(f"🎮 Tiempo jugado HOY: {horas_hoy:.1f} horas ({minutos_hoy:.0f} minutos)\n")
                f.write(f"📅 Fecha del reporte: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"📈 Tiempo total esta SEMANA: {horas_semanal:.1f} horas\n")
                f.write("=" * 50 + "\n")
                f.write("📅 HISTORIAL RECIENTE:\n")
                
                # Mostrar últimos 7 días
                for fecha, segundos in list(self.data['historial'].items())[-7:]:
                    horas = segundos / 3600
                    fecha_formateada = datetime.datetime.fromisoformat(fecha).strftime('%d/%m')
                    f.write(f"   {fecha_formateada}: {horas:.1f} horas\n")
                    
                f.write("\n")
                f.write("⚠️  Este reporte se actualiza automáticamente\n")
                f.write("📍 Servicio: Monitor de Tiempo LOL\n")
                
        except Exception as e:
            pass

    def is_league_running(self):
        """Detectar si League of Legends está ejecutándose"""
        try:
            for process in psutil.process_iter(['name']):
                try:
                    nombre_proceso = process.info['name'].lower()
                    # Procesos relacionados con League of Legends
                    procesos_lol = ['league', 'riot', 'lolclient']
                    if any(proceso in nombre_proceso for proceso in procesos_lol):
                        return True
                except:
                    continue
        except:
            pass
        return False

    def track_time(self):
        """Monitorear el tiempo de juego"""
        try:
            if self.is_league_running():
                if self.current_session_start is None:
                    # LOL acaba de iniciar
                    self.current_session_start = time.time()
            else:
                if self.current_session_start is not None:
                    # LOL acaba de cerrarse
                    duracion_sesion = time.time() - self.current_session_start
                    self.data['tiempo_hoy'] += duracion_sesion
                    self.current_session_start = None
                    self.save_data()  # Guardar y generar reporte
        except:
            pass

    def SvcStop(self):
        """Método para detener el servicio"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)
        self.save_data()  # Guardar datos antes de cerrar

    def SvcDoRun(self):
        """Método principal de ejecución del servicio"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        # Esperar 30 segundos para que el sistema esté estable
        time.sleep(30)
        self.main()

    def main(self):
        """Bucle principal del servicio"""
        while self.is_running:
            # Esperar 60 segundos o hasta que se detenga el servicio
            if win32event.WaitForSingleObject(self.hWaitStop, 60000) == win32event.WAIT_OBJECT_0:
                break
            
            # Monitorear el tiempo
            self.track_time()
            
            # Verificar si es medianoche para resetear contador diario
            ahora = datetime.datetime.now()
            if ahora.hour == 0 and ahora.minute == 0:
                self.data['tiempo_hoy'] = 0
                self.save_data()
                time.sleep(61)  # Esperar para no resetear múltiples veces

if __name__ == '__main__':
    # Punto de entrada para el servicio Windows
    win32serviceutil.HandleCommandLine(LolTimeTrackerService)