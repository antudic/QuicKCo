# coding=utf-8
# pynput
# Copyright (C) 2015-2022 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import contextlib
import ctypes
import itertools

from ctypes import (
    windll,
    wintypes)

import win32_vks as VK

MapVirtualKey = windll.user32.MapVirtualKeyW
MapVirtualKey.argtypes = (
    wintypes.UINT,
    wintypes.UINT)
MapVirtualKey.MAPVK_VK_TO_VSC = 0

GetCurrentThreadId = windll.kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = wintypes.DWORD


class KeyTranslator(object):
    """A class to translate virtual key codes to characters.
    """
    _GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState
    _GetAsyncKeyState.argtypes = (
        ctypes.c_int,)
    
    _GetKeyboardLayout = ctypes.windll.user32.GetKeyboardLayout
    _GetKeyboardLayout.argtypes = (
        wintypes.DWORD,)
    
    _GetKeyboardState = ctypes.windll.user32.GetKeyboardState
    _GetKeyboardState.argtypes = (
        ctypes.c_voidp,)
    
    _GetKeyState = ctypes.windll.user32.GetAsyncKeyState
    _GetKeyState.argtypes = (
        ctypes.c_int,)
    
    _MapVirtualKeyEx = ctypes.windll.user32.MapVirtualKeyExW
    _MapVirtualKeyEx.argtypes = (
        wintypes.UINT,
        wintypes.UINT,
        wintypes.HKL)
    
    _ToUnicodeEx = ctypes.windll.user32.ToUnicodeEx
    _ToUnicodeEx.argtypes = (
        wintypes.UINT,
        wintypes.UINT,
        ctypes.c_voidp,
        ctypes.c_voidp,
        ctypes.c_int,
        wintypes.UINT,
        wintypes.HKL)

    _MAPVK_VK_TO_VSC = 0
    _MAPVK_VSC_TO_VK = 1
    _MAPVK_VK_TO_CHAR = 2

    def __init__(self):
        self.update_layout()
        self._modifier_state = [False, False, False] # shift, ctrl, alt
        self.keyIndex = {0x10: 0, 0xA0: 0, 0xA1: 0,
                         0x11: 1, 0xA2: 1, 0xA3: 1,
                         0x12: 2, 0xA4: 2, 0xA5: 2}

    def __call__(self, vk, scan, is_press):
        """Converts a virtual key code to a string.

        :param int vk: The virtual key code.

        :param bool is_press: Whether this is a press.

        :return: parameters suitable for the :class:`pynput.keyboard.KeyCode`
            constructor

        :raises OSError: if a call to any *win32* function fails
        """
        # Get a string representation of the key
        try: self._modifier_state[self.keyIndex[vk]] = is_press
        except KeyError: pass
        
        layout_data = self._layout_data[tuple(self._modifier_state)]
                
        try: character, is_dead = layout_data[scan]
        except: character, is_dead = None, None

        return {
            "char": character,
            "scan": scan,
            "vkCode": vk,
            "vkName": VK.vkName.get(vk),
            "is_press": is_press
            }

    def update_layout(self):
        """Updates the cached layout data.
        """
        self._layout, self._layout_data = self._generate_layout()

    def char_from_scan(self, scan):
        """Translates a scan code to a character, if possible.

        :param int scan: The scan code to translate.

        :return: maybe a character
        :rtype: str or None
        """
        return self._layout_data[(False, False, False)][scan][0]

    def _generate_layout(self):
        """Generates the keyboard layout.

        This method will call ``ToUnicodeEx``, which modifies kernel buffers,
        so it must *not* be called from the keyboard hook.

        The return value is the tuple ``(layout_handle, layout_data)``, where
        ``layout_data`` is a mapping from the tuple ``(shift, ctrl, alt)`` to
        an array indexed by scan code containing the data
        ``(character, is_dead)``, and ``layout_handle`` is the handle of the
        layout.

        :return: a composite layout
        """
        layout_data = {}

        state = (ctypes.c_ubyte * 255)()
        with self._thread_input() as active_thread:
            layout = self._GetKeyboardLayout(active_thread)
        vks = [
            self._to_vk(scan, layout)
            for scan in range(len(state))]

        for shift, ctrl, alt in itertools.product(
                (False, True), (False, True), (False, True)):
            current = [(None, False)] * len(state)
            layout_data[(shift, ctrl, alt)] = current

            # Update the keyboard state based on the modifier state
            state[VK.SHIFT] = 0x80 if shift else 0x00
            state[VK.CONTROL] = 0x80 if ctrl else 0x00
            state[VK.MENU] = 0x80 if alt else 0x00

            # For each virtual key code...
            out = (ctypes.wintypes.WCHAR * 5)()
            for (scan, vk) in enumerate(vks):
                # ...translate it to a unicode character
                count = self._ToUnicodeEx(
                    vk, scan, ctypes.byref(state), ctypes.byref(out),
                    len(out), 0, layout)

                # Cache the result if a key is mapped
                if count != 0:
                    character = out[0]
                    is_dead = count < 0
                    current[scan] = (character, is_dead)

                    # If the key is dead, flush the keyboard state
                    if is_dead:
                        self._ToUnicodeEx(
                            vk, scan, ctypes.byref(state),
                            ctypes.byref(out), len(out), 0, layout)

        return (layout, layout_data)

    def _to_vk(self, scan, layout):
        """Retrieves the virtual key code for a scan code.

        :param int vscan: The scan code.

        :param layout: The keyboard layout.

        :return: the virtual key code
        """
        return self._MapVirtualKeyEx(
            scan, self._MAPVK_VSC_TO_VK, layout)
    

    @contextlib.contextmanager
    def _thread_input(self):
        """Yields the current thread ID.
        """
        yield GetCurrentThreadId()
