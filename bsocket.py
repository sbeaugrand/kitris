# ---------------------------------------------------------------------------- #
## \file bsocket.py
## \author Sebastien Beaugrand
## \sa http://beaugrand.chez.com/
## \copyright CeCILL 2.1 Free Software license
# ---------------------------------------------------------------------------- #
from abc import ABC, abstractmethod
from kivy.utils import platform
if platform == 'android':
    from jnius import autoclass
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    UUID = autoclass('java.util.UUID')
else:
    from bluetooth import *
    import pydbus

COUNT_MIN = 33
COUNT_MAX = 125
KITRIS_UUID = '00031111-0000-1000-8000-00805F9B34FB'


# ---------------------------------------------------------------------------- #
## \class BSocket
# ---------------------------------------------------------------------------- #
class BSocket(ABC):
    def __init__(self):
        self.socket = None

    def __del__(self):
        self.close()

    def instance():
        if platform == 'android':
            return ABSocket()
        else:
            return LBSocket()

    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
            print('info: socket closed')

    def paired():
        l = list()
        if platform == 'android':
            paired_devices = BluetoothAdapter.getDefaultAdapter(
            ).getBondedDevices().toArray()
            for d in paired_devices:
                l.append((d.getName(), d))
        else:
            bus = pydbus.SystemBus()
            mngr = bus.get('org.bluez', '/')
            mng_objs = mngr.GetManagedObjects()
            for path in mng_objs:
                if mng_objs[path].get('org.bluez.Device1',
                                      {}).get('Paired', []):
                    name = mng_objs[path].get('org.bluez.Device1',
                                              {}).get('Name', [])
                    addr = mng_objs[path].get('org.bluez.Device1',
                                              {}).get('Address', [])
                    l.append((name, addr))
        return l

    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def create(self, name):
        pass

    @abstractmethod
    def send(self, cmd):
        pass

    @abstractmethod
    def recv(self):
        pass


# ---------------------------------------------------------------------------- #
## \class ABSocket
# ---------------------------------------------------------------------------- #
class ABSocket(BSocket):
    last_r = ''

    def listen(self):
        try:
            server_socket = BluetoothAdapter.getDefaultAdapter(
            ).listenUsingInsecureRfcommWithServiceRecord(
                'kitris', UUID.fromString(KITRIS_UUID))
            print('listen: waiting for connection')
            self.socket = server_socket.accept()
            self.recv_stream = self.socket.getInputStream()
            self.send_stream = self.socket.getOutputStream()
            server_socket.close()
        except Exception as e:
            print('listen: {}'.format(e))
            return False
        return True

    def create(self, name):
        for device in BSocket.paired():
            if device[0] == name:
                self.socket = device[
                    1].createInsecureRfcommSocketToServiceRecord(
                        UUID.fromString(KITRIS_UUID))
                self.recv_stream = self.socket.getInputStream()
                self.send_stream = self.socket.getOutputStream()
                try:
                    self.socket.connect()
                    return True
                except Exception as e:
                    print('connect: {}'.format(e))
        return False

    def send(self, cmd):
        try:
            self.send_stream.write(bytes(cmd + ' ', 'ascii'))
        except Exception as e:
            print('send: {}'.format(e))

    def recv(self):
        l = list()
        try:
            if self.recv_stream.available() == 0:
                return l
            r = bytearray(0)
            while True:
                r2 = bytearray(b'~' * 20)
                if self.recv_stream.read(r2) < 20:
                    r += r2
                    break
                r += r2
            for i in r.split(b'~')[0].split():
                b = str(i, 'ascii')
                l.append(b)
            self.last_r = r
        except Exception as e:
            print('recv: {}'.format(e))
        return l


# ---------------------------------------------------------------------------- #
## \class LBSocket
# ---------------------------------------------------------------------------- #
class LBSocket(BSocket):
    def __init__(self):
        super(LBSocket, self).__init__()

    def __del__(self):
        super(LBSocket, self).__del__()

    def listen(self):
        server_socket = BluetoothSocket(RFCOMM)
        server_socket.bind(('', PORT_ANY))
        server_socket.listen(1)
        port = server_socket.getsockname()[1]
        advertise_service(server_socket,
                          'kitris',
                          service_id=KITRIS_UUID,
                          service_classes=[KITRIS_UUID, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE])
        print('listen: waiting for connection')
        self.socket, _ = server_socket.accept()
        self.socket.settimeout(0.02)
        server_socket.close()
        return True

    def create(self, name):
        for device in BSocket.paired():
            if device[0] == name:
                service_matches = find_service(name='kitris',
                                               uuid=KITRIS_UUID,
                                               address=device[1])
                if len(service_matches) == 0:
                    print('error: service not found')
                    return False
                first_match = service_matches[0]
                port = first_match['port']
                name = first_match['name']
                host = first_match['host']
                self.socket = BluetoothSocket(RFCOMM)
                print('connect: connecting to "{}" on {}'.format(name, host))
                try:
                    self.socket.connect((host, port))
                    self.socket.settimeout(0.02)
                    return True
                except Exception as e:
                    print('connect: {}'.format(e))
        return False

    def send(self, cmd):
        try:
            self.socket.send(bytes(cmd + ' ', 'ascii'))
        except Exception as e:
            print('send: {}'.format(e))

    def recv(self):
        l = list()
        try:
            r = self.socket.recv(200)
            for i in r.split():
                b = str(i, 'ascii')
                l.append(b)
        except btcommon.BluetoothError:
            pass
        except Exception as e:
            print('recv: {}'.format(e))
        return l
