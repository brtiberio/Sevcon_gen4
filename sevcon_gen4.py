#!/usr/bin/python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2019 Bruno Tibério
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import canopen
import logging
import sys


class SevconGen4:
    """
    TODO
    """

    channel = 'can0'
    bustype = 'socketcan'
    nodeID = 2
    network = None
    _connected = False

    # If EDS file is present, this is not necessary, all codes can be gotten
    # from object dictionary.
    object_index = {'Device Type': 0x1000,
                   'Error Register': 0x1001,
                   'Error History': 0x1003,
                   'COB-ID SYNC Message': 0x1005,
                   'Device Name': 0x1008,
                   'Guard Time': 0x100C,
                   'Life Time Factor': 0x100D,
                   'Store Parameters': 0x1010,
                   'Restore Default Parameters': 0x1011,
                   'COB-ID Emergency Object': 0x1014,
                   'Consumer Heartbeat Time': 0x1016,
                   'Producer Heartbeat Time': 0x1017,
                   'Identity Object': 0x1018,
                   'Verify configuration': 0x1020,
                   'Server SDO 1 Parameter': 0x1200,
                   'Receive PDO 1 Parameter': 0x1400,
                   'Receive PDO 2 Parameter': 0x1401,
                   'Receive PDO 3 Parameter': 0x1402,
                   'Receive PDO 4 Parameter': 0x1403,
                   'Receive PDO 1 Mapping': 0x1600,
                   'Receive PDO 2 Mapping': 0x1601,
                   'Receive PDO 3 Mapping': 0x1602,
                   'Receive PDO 4 Mapping': 0x1603,
                   'Transmit PDO 1 Parameter': 0x1800,
                   'Transmit PDO 2 Parameter': 0x1801,
                   'Transmit PDO 3 Parameter': 0x1802,
                   'Transmit PDO 4 Parameter': 0x1803,
                   'Transmit PDO 1 Mapping': 0x1A00,
                   'Transmit PDO 2 Mapping': 0x1A01,
                   'Transmit PDO 3 Mapping': 0x1A02,
                   'Transmit PDO 4 Mapping': 0x1A03,
                   'Node ID': 0x2000,
                   'CAN Bitrate': 0x2001,
                   'RS232 Baudrate': 0x2002,
                   'Version Numbers': 0x2003,
                   'Serial Number': 0x2004,
                   'RS232 Frame Timeout': 0x2005,
                   'Miscellaneous Configuration': 0x2008,
                   'Internal Dip Switch State': 0x2009,
                   'Custom persistent memory': 0x200C,
                   'Internal DataRecorder Control': 0x2010,
                   'Internal DataRecorder Configuration': 0x2011,
                   'Internal DataRecorder Sampling Period': 0x2012,
                   'Internal DataRecorder Number of Preceding Samples': 0x2013,
                   'Internal DataRecorder Number of Sampling Variables': 0x2014,
                   'DataRecorder Index of Variables': 0x2015,
                   'Internal DataRecorder SubIndex of Variables': 0x2016,
                   'Internal DataRecorder Status': 0x2017,
                   'Internal DataRecorder Max Number of Samples': 0x2018,
                   'Internal DataRecorder Number of Recorded Samples': 0x2019,
                   'Internal DataRecorder Vector Start Offset': 0x201A,
                   'Encoder Counter': 0x2020,
                   'Encoder Counter at Index Pulse': 0x2021,
                   'Hallsensor Pattern': 0x2022,
                   'Internal Object Demand Rotor Angle': 0x2023,
                   'Internal System State': 0x2024,
                   'Internal Object Reserved': 0x2025,
                   'Internal Object ProcessMemory': 0x2026,
                   'Current Actual Value Averaged': 0x2027,
                   'Velocity Actual Value Averaged': 0x2028,
                   'Internal Object Actual Rotor Angle': 0x2029,
                   'Internal Object NTC Temperature Sensor Value': 0x202A,
                   'Internal Object Motor Phase Current U': 0x202B,
                   'Internal Object Motor Phase Current V': 0x202C,
                   'Internal Object Measured Angle Difference': 0x202D,
                   'Trajectory Profile Time': 0x202E,
                   'CurrentMode Setting Value': 0x2030,
                   'PositionMode Setting Value': 0x2062,
                   'VelocityMode Setting Value': 0x206B,
                   'Configuration Digital Inputs': 0x2070,
                   'Digital Input Funtionalities': 0x2071,
                   'Position Marker': 0x2074,
                   'Digital Output Funtionalities': 0x2078,
                   'Configuration Digital Outputs': 0x2079,
                   'Analog Inputs': 0x207C,
                   'Current Threshold for Homing Mode': 0x2080,
                   'Home Position': 0x2081,
                   'Following Error Actual Value': 0x20F4,
                   'Sensor Configuration': 0x2210,
                   'Digital Position Input': 0x2300,
                   'Internal Object Download Area': 0x2FFF,
                   'ControlWord': 0x6040,
                   'StatusWord': 0x6041,
                   'Modes of Operation': 0x6060,
                   'Modes of Operation Display': 0x6061,
                   'Position Demand Value': 0x6062,
                   'Position Actual Value': 0x6064,
                   'Max Following Error': 0x6065,
                   'Position Window': 0x6067,
                   'Position Window Time': 0x6068,
                   'Velocity Sensor Actual Value': 0x6069,
                   'Velocity Demand Value': 0x606B,
                   'Velocity Actual Value': 0x606C,
                   'Current Actual Value': 0x6078,
                   'Target Position': 0x607A,
                   'Home Offset': 0x607C,
                   'Software Position Limit': 0x607D,
                   'Max Profile Velocity': 0x607F,
                   'Profile Velocity': 0x6081,
                   'Profile Acceleration': 0x6083,
                   'Profile Deceleration': 0x6084,
                   'QuickStop Deceleration': 0x6085,
                   'Motion ProfileType': 0x6086,
                   'Position Notation Index': 0x6089,
                   'Position Dimension Index': 0x608A,
                   'Velocity Notation Index': 0x608B,
                   'Velocity Dimension Index': 0x608C,
                   'Acceleration Notation Index': 0x608D,
                   'Acceleration Dimension Index': 0x608E,
                   'Homing Method': 0x6098,
                   'Homing Speeds': 0x6099,
                   'Homing Acceleration': 0x609A,
                   'Current Control Parameter': 0x60F6,
                   'Speed Control Parameter': 0x60F9,
                   'Position Control Parameter': 0x60FB,
                   'TargetVelocity': 0x60FF,
                   'MotorType': 0x6402,
                   'Motor Data': 0x6410,
                   'Supported Drive Modes': 0x6502}
    # CANopen defined error codes and Maxon codes also
    error_index = {0x00000000: 'Error code: no error',
                  # 0x050x xxxx
                  0x05030000: 'Error code: toggle bit not alternated',
                  0x05040000: 'Error code: SDO protocol timeout',
                  0x05040001: 'Error code: Client/server command specifier not valid or unknown',
                  0x05040002: 'Error code: invalid block size',
                  0x05040003: 'Error code: invalid sequence number',
                  0x05040004: 'Error code: CRC error',
                  0x05040005: 'Error code: out of memory',
                  # 0x060x xxxx
                  0x06010000: 'Error code: Unsupported access to an object',
                  0x06010001: 'Error code: Attempt to read a write-only object',
                  0x06010002: 'Error code: Attempt to write a read-only object',
                  0x06020000: 'Error code: object does not exist',
                  0x06040041: 'Error code: object can not be mapped to the PDO',
                  0x06040042: 'Error code: the number and length of the objects to be mapped would exceed PDO length',
                  0x06040043: 'Error code: general parameter incompatibility',
                  0x06040047: 'Error code: general internal incompatibility in the device',
                  0x06060000: 'Error code: access failed due to an hardware error',
                  0x06070010: 'Error code: data type does not match, length of service parameter does not match',
                  0x06070012: 'Error code: data type does not match, length of service parameter too high',
                  0x06070013: 'Error code: data type does not match, length of service parameter too low',
                  0x06090011: 'Error code: subindex does not exist',
                  0x06090030: 'Error code: value range of parameter exceeded',
                  0x06090031: 'Error code: value of parameter written is too high',
                  0x06090032: 'Error code: value of parameter written is too low',
                  0x06090036: 'Error code: maximum value is less than minimum value',
                  0x060A0023: 'Error code: resource not available: SDO connection',
                  # 0x0800 xxxx
                  0x08000000: 'Error code: General error',
                  0x08000020: 'Error code: Data cannot be transferred or stored to the application',
                  0x08000021: 'Error code: Data cannot be transferred or stored to the application because of local control',
                  0x08000022: 'Error code: Wrong Device State. Data can not be transfered',
                  0x08000023: 'Error code: Object dictionary dynamic generation failed or no object dictionary present',
                  # Maxon defined error codes
                  0x0f00ffc0: 'Error code: wrong NMT state',
                  0x0f00ffbf: 'Error code: rs232 command illegal',
                  0x0f00ffbe: 'Error code: password incorrect',
                  0x0f00ffbc: 'Error code: device not in service mode',
                  0x0f00ffB9: 'Error code: error in Node-ID'
                  }
    # dictionary describing opMode
    opModes = {4: 'Torque Profile Mode', 3: 'Profile Velocity Mode', 1: 'Profile Position Mode',
               2: 'Velocity Mode', 5: 'Voltage Mode', 6: 'Homing Mode', 7: 'Interpolated Position Mode'}
    node = []
    # dictionary object to describe state of EPOS device
    state = {0: 'start', 1: 'not ready to switch on', 2: 'switch on disable',
             3: 'ready to switch on', 4: 'switched on', 5: 'refresh',
             6: 'measure init', 7: 'operation enable', 8: 'quick stop active',
             9: 'fault reaction active (disabled)', 10: 'fault reaction active (enable)', 11: 'fault',
             -1: 'Unknown'}

    def __init__(self, _network=None, debug=False):
        """ Init function

        Args:
            _network: if already defined, use the shared network
            debug:  Log with debug level or not
        Return:
             Object: An instantiated class object of type SevconGen4
        """
        # check if network is passed over or create a new one
        if not _network:
            self.network = canopen.Network()
        else:
            self.network = _network

        self.logger = logging.getLogger('Sevcon')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def begin(self, nodeID, _channel='can0', _bustype='socketcan', object_dictionary=None):
        """ Initialize Sevcon device

        Configure and setup Epos device.

        Args:
            nodeID:    Node ID of the device.
            channel (optional):   Port used for communication. Default can0
            bustype (optional):   Port type used. Default socketcan.
            object_dictionary (optional):   Name of EDS file, if any available.
        Return:
            bool: A boolean if all went ok.
        """
        try:
            self.node = self.network.add_node(
                nodeID, object_dictionary=object_dictionary)
            # in not connected?
            if not self.network.bus:
                # so try to connect
                self.network.connect(channel=_channel, bustype=_bustype)
        except Exception as e:
            self.log_info('Exception caught:{0}'.format(str(e)))
        finally:
            # check if is connected
            if not self.network.bus:
                self._connected = False
            else:
                self._connected = True
            return self._connected

    def disconnect(self):
        self.network.disconnect()
        return
        # --------------------------------------------------------------
        # Basic set of functions
        # --------------------------------------------------------------

    def log_info(self, message=None):
        """ Log a message

        A wrap around logging.
        The log message will have the following structure\:
        [class name \: function name ] message

        Args:
            message: a string with the message.
        """
        if message is None:
            # do nothing
            return
        self.logger.info('[{0}:{1}] {2}'.format(
            self.__class__.__name__,
            sys._getframe(1).f_code.co_name,
            message))
        return

    def log_debug(self, message=None):
        """ Log a message

        A wrap around logging.
        The log message will have the following structure\:
        [class name \: function name ] message

        the function name will be the caller function retrieved automatically
        by using sys._getframe(1).f_code.co_name

        Args:
            message: a string with the message.
        """
        if message is None:
            # do nothing
            return

        self.logger.debug('[{0}:{1}] {2}'.format(
            self.__class__.__name__,
            sys._getframe(1).f_code.co_name,
            message))
        return

    def read_object(self, index, subindex):
        """Reads an object

         Request a read from dictionary object referenced by index and subindex.

         Args:
             index:     reference of dictionary object index
             subindex:  reference of dictionary object subindex
         Returns:
             bytes:  message returned by EPOS or empty if unsucessfull
        """
        if self._connected:
            try:
                return self.node.sdo.upload(index, subindex)
            except Exception as e:
                self.log_info('Exception caught:{0}'.format(str(e)))
                return None
        else:
            self.log_info(' Error: {0} is not connected'.format(
                self.__class__.__name__))
            return None

    def write_object(self, index, subindex, data):
        """Write an object

         Request a write to dictionary object referenced by index and subindex.

         Args:
             index:     reference of dictionary object index
             subindex:  reference of dictionary object subindex
             data:      data to be stored
         Returns:
             bool:      boolean if all went ok or not
        """
        if self._connected:
            try:
                self.node.sdo.download(index, subindex, data)
                return True
            except canopen.SdoAbortedError as e:
                text = "Code 0x{:08X}".format(e.code)
                if e.code in self.error_index:
                    text = text + ", " + self.error_index[e.code]
                self.log_info('SdoAbortedError: ' + text)
                return False
            except canopen.SdoCommunicationError:
                self.log_info('SdoAbortedError: Timeout or unexpected response')
                return False
        else:
            self.log_info(' Error: {0} is not connected'.format(
                self.__class__.__name__))
            return False

    ############################################################################
    # High level functions
    ############################################################################

    def read_statusword(self):
        """Read StatusWord

        Request current statusword from device.

        Returns:
            tupple: A tupple containing:

            :statusword:  the current statusword or None if any error.
            :Ok: A boolean if all went ok.
        """
        index = self.object_index['StatusWord']
        subindex = 0
        statusword = self.read_object(index, subindex)
        # failded to request?
        if not statusword:
            self.log_info('Error trying to read {0} statusword'.format(
                self.__class__.__name__))
            return statusword, False

        # return statusword as an int type
        statusword = int.from_bytes(statusword, 'little')
        return statusword, True

    def read_control_word(self):
        """Read ControlWord

        Request current controlword from device.

        Returns:
            tupple: A tupple containing:

            :controlword: the current controlword or None if any error.
            :Ok: A boolean if all went ok.
        """
        index = self.object_index['ControlWord']
        subindex = 0
        controlword = self.read_object(index, subindex)
        # failded to request?
        if not controlword:
            self.log_info('Error trying to read {0} controlword'.format(
                self.__class__.__name__))
            return controlword, False

        # return controlword as an int type
        controlword = int.from_bytes(controlword, 'little')
        return controlword, True

    def write_control_word(self, controlword):
        """Send controlword to device

        Args:
            controlword: word to be sent.

        Returns:
            bool: a boolean if all went ok.
        """
        # sending new controlword
        self.log_debug(
            'Sending controlword Hex={0:#06X} Bin={0:#018b}'.format(controlword))
        controlword = controlword.to_bytes(2, 'little')
        return self.write_object(0x6040, 0, controlword)

    def check_state(self):
        """Check current state of Epos

        Ask the StatusWord of EPOS and parse it to return the current state of EPOS.

        +----------------------------------+-----+---------------------+
        | State                            | ID  | Statusword [binary] |
        +==================================+=====+=====================+
        | Start                            | 0   | xxxx xxxx  0000 0000|
        +----------------------------------+-----+---------------------+
        | Not Ready to Switch On           | 1   | xxxx xxxx  00x0 0000|
        +----------------------------------+-----+---------------------+
        | Switch on disabled               | 2   | xxxx xxxx  01x0 0000|
        +----------------------------------+-----+---------------------+
        | ready to switch on               | 3   | xxxx xxxx  001x 0001|
        +----------------------------------+-----+---------------------+
        | switched on                      | 4   | xxxx xxxx  001x 0011|
        +----------------------------------+-----+---------------------+
        | refresh                          | 5   | x1xx xxx1  x010 0011|
        +----------------------------------+-----+---------------------+
        | measure init                     | 6   | x1xx xxx1  x011 0011|
        +----------------------------------+-----+---------------------+
        | operation enable                 | 7   | xxxx xxxx  001x 0111|
        +----------------------------------+-----+---------------------+
        | quick stop active                | 8   | xxxx xxxx  xxxx 0111|
        +----------------------------------+-----+---------------------+
        | fault reaction active (disabled) | 9   | x0xx xxx1  x000 1111|
        +----------------------------------+-----+---------------------+
        | fault reaction active (enabled)  | 10  | x0xx xxx1  x001 1111|
        +----------------------------------+-----+---------------------+
        | Fault                            | 11  | 0000 0000  00x0 1000|
        +----------------------------------+-----+---------------------+

        see section 8.1.1 of firmware manual for more details.

        Returns:
            int: numeric identification of the state or -1 in case of fail.
        """
        statusword, ok = self.read_statusword()
        if not ok:
            self.log_info('Failed to request StatusWord')
            return -1
        else:
            statusword = statusword & 0xFF
            # state 'start' (0)
            # statusWord == 0000 0000
            bitmask = 0b11111111
            if(bitmask & statusword == 0):
                ID = 0
                return ID

        # state 'not ready to switch on' (1)
        # statusWord == 00x0 0000
            bitmask = 0b11011111
            if (bitmask & statusword == 32):
                ID = 1
                return ID

            # state 'switch on disabled' (2)
            # statusWord == 01x0 0000
            bitmask = 0b11011111
            if(bitmask & statusword == 64):
                ID = 2
                return ID

            # state 'ready to switch on' (3)
            # statusWord == 001x 0001
            bitmask = 0b11101111
            if(bitmask & statusword == 33):
                ID = 3
                return ID

            # state 'switched on' (4)
            # statusWord == 001x 0011
            bitmask = 0b11101111
            if(bitmask & statusword == 35):
                ID = 4
                return ID

            # state 'refresh' (5)
            # statusWord == x1xx xxx1  x010 0011
            #bitmask = 0b0100000101111111
            #if(bitmask & statusword == 16675):
            #    ID = 5
            #    return ID

            # state 'measure init' (6)
            # statusWord == x1xx xxx1  x011 0011
            #bitmask = 0b0100000101111111
            #if(bitmask & statusword == 16691):
            #    ID = 6
            #    return ID
            # state 'operation enable' (7)
            # statusWord == 001x 0111
            bitmask = 0b11101111
            if(bitmask & statusword == 39):
                ID = 7
                return ID

            # state 'Quick Stop Active' (8)
            # statusWord == xxxx 0111
            bitmask = 0b00001111
            if(bitmask & statusword == 7):
                ID = 8
                return ID

            # state 'fault reaction active (disabled)' (9)
            # statusWord == x0xx xxx1  x000 1111
            #bitmask = 0b0100000101111111
            #if(bitmask & statusword == 271):
            #    ID = 9
            #    return ID

            # state 'fault reaction active (enabled)' (10)
            # statusWord == x0xx xxx1  x001 1111
            #bitmask = 0b0100000101111111
            #if(bitmask & statusword == 287):
            #    ID = 10
            #   return ID

            # state 'fault' (11)
            # statusWord == 00x0 1000
            bitmask = 0b11011111
            if(bitmask & statusword == 8):
                ID = 11
                return ID

        # in case of unknown state or fail
        # in case of unknown state or fail
        self.logInfo('Error: Unknown state. Statusword is Bin={0:#018b}'.format(
            int.from_bytes(statusword, 'little'))
        )
        return -1

    def print_state(self):
        ID = self.check_state()
        if ID is -1:
            print('[{0}:{1}] Error: Unknown state\n'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name))
        else:
            print('[{0}:{1}] Current state [ID]:{2} [{3}]\n'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                self.state[ID],
                ID))
        return

    def print_statusword(self):
        statusword, Ok = self.read_statusword()
        if not Ok:
            print('[{0}:{1}] Failed to retreive statusword\n'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name))
            return
        else:
            print("[{0}:{1}] The statusword is Hex={2:#06X} Bin={2:#018b}\n".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                statusword))
            print('Bit 15: undefined                                              {0}'.format(
                (statusword & (1 << 15)) >> 15))
            print('Bit 14: undefined                                              {0}'.format(
                (statusword & (1 << 14)) >> 14))
            print('Bit 13: undefined                                              {0}'.format(
                (statusword & (1 << 13)) >> 13))
            print('Bit 12: OpMode specific: [Set-point ack|Speed|Homing attained] {0}'.format(
                (statusword & (1 << 12)) >> 12))
            print('Bit 11: Internal limit active:                                 {0}'.format(
                (statusword & (1 << 11)) >> 11))
            print('Bit 10: Target reached:                                        {0}'.format(
                (statusword & (1 << 10)) >> 10))
            print('Bit 09: Remote (NMT Slave State Operational):                  {0}'.format(
                (statusword & (1 << 9)) >> 9))
            print('Bit 08: undefined                                              {0}'.format(
                (statusword & (1 << 8)) >> 8))
            print('Bit 07: Warning:                                               {0}'.format(
                (statusword & (1 << 7)) >> 7))
            print('Bit 06: Switch on disable:                                     {0}'.format(
                (statusword & (1 << 6)) >> 6))
            print('Bit 05: Quick stop:                                            {0}'.format(
                (statusword & (1 << 5)) >> 5))
            print('Bit 04: Voltage enabled (power stage on):                      {0}'.format(
                (statusword & (1 << 4)) >> 4))
            print('Bit 03: Fault:                                                 {0}'.format(
                (statusword & (1 << 3)) >> 3))
            print('Bit 02: Operation enable:                                      {0}'.format(
                (statusword & (1 << 2)) >> 2))
            print('Bit 01: Switched on:                                           {0}'.format(
                (statusword & (1 << 1)) >> 1))
            print('Bit 00: Ready to switch on:                                    {0}'.format(
                statusword & 1))
        return

    def print_controlword(self, controlword=None):
        """Print the meaning of controlword

        Check the meaning of current controlword of device or check the meaning of your own controlword.
        Usefull to check your own controlword before actually sending it to device.

        Args:
            controlword (optional): If None, request the controlword of device.

        """
        if not controlword:
            controlword, Ok = self.read_controlword()
            if not Ok:
                print('[{0}:{1}] Failed to retreive controlword\n'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name))
                return
        print("[{0}:{1}] The controlword is Hex={2:#06X} Bin={2:#018b}\n".format(
            self.__class__.__name__,
            sys._getframe().f_code.co_name,
            controlword))
        # Bit 15 to 11 not used, 10 to 9 reserved
        print('Bit 08: Halt:                                                                   {0}'.format(
            (controlword & (1 << 8)) >> 8))
        print('Bit 07: Fault reset:                                                            {0}'.format(
            (controlword & (1 << 7)) >> 7))
        print('Bit 06: Operation mode specific:[Abs=0|rel=1]                                   {0}'.format(
            (controlword & (1 << 6)) >> 6))
        print('Bit 05: Operation mode specific:[Change set immediately]                        {0}'.format(
            (controlword & (1 << 5)) >> 5))
        print('Bit 04: Operation mode specific:[New set-point|reserved|Homing operation start] {0}'.format(
            (controlword & (1 << 4)) >> 4))
        print('Bit 03: Enable operation:                                                       {0}'.format(
            (controlword & (1 << 3)) >> 3))
        print('Bit 02: Quick stop:                                                             {0}'.format(
            (controlword & (1 << 2)) >> 2))
        print('Bit 01: Enable voltage:                                                         {0}'.format(
            (controlword & (1 << 1)) >> 1))
        print('Bit 00: Switch on:                                                              {0}'.format(
            controlword & 1))
        return


def main():
    """Test Sevcon Gen4 CANopen communication with some examples.

    Use a few examples to test communication with Sevcon device using
    a few functions. Also resets the fault error if present.

    Show sample using also the EDS file.
    """

    import argparse
    if sys.version_info < (3, 0):
        print("Please use python version 3")
        return

    parser = argparse.ArgumentParser(add_help=True,
                                     description='Test Sevcon CANopen Communication')
    parser.add_argument('--channel', '-c', action='store', default='can0',
                        type=str, help='Channel to be used', dest='channel')
    parser.add_argument('--bus', '-b', action='store',
                        default='socketcan', type=str, help='Bus type', dest='bus')
    parser.add_argument('--rate', '-r', action='store', default=None,
                        type=int, help='bitrate, if applicable', dest='bitrate')
    parser.add_argument('--nodeID', action='store', default=1, type=int,
                        help='Node ID [ must be between 1- 127]', dest='nodeID')
    parser.add_argument('--objDict', action='store', default=None,
                        type=str, help='Object dictionary file', dest='objDict')
    args = parser.parse_args()

    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s.%(msecs)03d] [%(name)-20s]: %(levelname)-8s %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        filename='sevcon.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # instantiate object
    inverter = SevconGen4()

    if not (inverter.begin(args.nodeID, object_dictionary=args.objDict)):
        logging.info('Failed to begin connection with inverter device')
        logging.info('Exiting now')
        return

    # check if EDS file is supplied and print it
    if args.objDict:
        print('----------------------------------------------------------', flush=True)
        print('Printing EDS file entries')
        print('----------------------------------------------------------', flush=True)
        for obj in inverter.node.object_dictionary.values():
            print('0x%X: %s' % (obj.index, obj.name))
        if isinstance(obj, canopen.objectdictionary.Record):
            for subobj in obj.values():
                print('  %d: %s' % (subobj.subindex, subobj.name))
        print('----------------------------------------------------------', flush=True)
        # test record a single record
        error_log = inverter.node.sdo['Error History']
        # Iterate over arrays or record
        for error in error_log.values():
            print("Error 0x%X was found in the log" % error.raw)

        print('----------------------------------------------------------', flush=True)

    # use simple hex values
    # try to read status word
    statusword = inverter.read_object(0x6041, 0)
    if not statusword:
        print("Error trying to read Sevcon statusword\n")
        return
    else:
        print('----------------------------------------------------------', flush=True)
        print("The statusword is \n Hex={0:#06X} Bin={0:#018b}".format(
            int.from_bytes(statusword, 'little')))

    # test printStatusWord and state
    print('----------------------------------------------------------', flush=True)
    print('Testing print of StatusWord and State and ControlWord')
    print('----------------------------------------------------------', flush=True)
    inverter.print_state()
    print('----------------------------------------------------------', flush=True)
    inverter.print_statusword()
    print('----------------------------------------------------------', flush=True)
    # try to read controlword using hex codes
    controlword = inverter.read_object(0x6040, 0)
    if not controlword:
        logging.info("[EPOS] Error trying to read EPOS controlword\n")
    else:
        print("The controlword is \n Hex={0:#06X} Bin={0:#018b}".format(
            int.from_bytes(controlword, 'little')))
        print('----------------------------------------------------------', flush=True)
        # perform a reset, by using controlword
        controlword = int.from_bytes(controlword, 'little')
        controlword = (controlword | (1 << 7))
        print('----------------------------------------------------------', flush=True)
        print("The new controlword is \n Hex={0:#06X} Bin={0:#018b}".format(
            controlword))
        print('----------------------------------------------------------', flush=True)
        # sending new controlword
        controlword = controlword.to_bytes(2, 'little')
        inverter.write_object(0x6040, 0, controlword)
        # check led status to see if it is green and blinking

    inverter.disconnect()
    return


if __name__ == '__main__':
    main()
