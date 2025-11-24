# Third-Party Licenses

This document contains the licenses for third-party dependencies used in mdvupy.

---

## PySide6

**License**: LGPL v3 / Qt Commercial License  
**URL**: https://www.qt.io/licensing/  
**Version**: 6.7+

PySide6 is the official Python bindings for the Qt framework. mdvupy uses PySide6 under the LGPL v3 license, which allows use in proprietary applications as long as the library is dynamically linked (which it is in our case).

Qt and PySide6 are available under:
- LGPL v3 (open source)
- Commercial license (for proprietary use without LGPL restrictions)

For full license text, see: https://www.gnu.org/licenses/lgpl-3.0.html

---

## markdown-it-py

**License**: MIT  
**URL**: https://github.com/executablebooks/markdown-it-py  
**Version**: 3.0.0+

```
MIT License

Copyright (c) 2020 ExecutableBookProject

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## pyqtdarktheme

**License**: MIT  
**URL**: https://github.com/5yutan5/PyQtDarkTheme  
**Version**: 2.1.0+

```
MIT License

Copyright (c) 2021 Yunosuke Ohsugi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## loguru

**License**: MIT  
**URL**: https://github.com/Delgan/loguru  
**Version**: 0.7.3+

```
MIT License

Copyright (c) 2017 Delgan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## darkdetect

**License**: BSD 3-Clause  
**URL**: https://github.com/albertosottile/darkdetect  
**Version**: 0.7.1+

```
BSD 3-Clause License

Copyright (c) 2019, Alberto Sottile
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

---

## mdurl

**License**: MIT  
**URL**: https://github.com/executablebooks/mdurl  
**Version**: 0.1.2+

```
MIT License

Copyright (c) 2015 Vitaly Puzrin, Alex Kocharin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Development Dependencies

The following dependencies are used only during development and are not included in distributed builds:

### pytest

**License**: MIT  
**URL**: https://github.com/pytest-dev/pytest

### pytest-qt

**License**: MIT  
**URL**: https://github.com/pytest-dev/pytest-qt

### ruff

**License**: MIT  
**URL**: https://github.com/astral-sh/ruff

### mkdocs

**License**: BSD  
**URL**: https://www.mkdocs.org/

---

## Build Tools

### PyInstaller

**License**: GPL v2 with exception  
**URL**: https://www.pyinstaller.org/

PyInstaller is licensed under GPL v2, but includes an exception that allows bundled applications to be distributed under any license. The exception means you can distribute your bundled application (mdvupy) under the MIT license without GPL restrictions.

For full license text, see: https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt

---

## Summary

All runtime dependencies use permissive licenses (MIT, BSD, LGPL) that allow use in proprietary applications:

- **PySide6**: LGPL v3 (dynamically linked)
- **markdown-it-py**: MIT
- **pyqtdarktheme**: MIT
- **loguru**: MIT
- **darkdetect**: BSD 3-Clause
- **mdurl**: MIT

Development and build tools use compatible licenses that do not affect distribution.
