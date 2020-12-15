#!/usr/bin/env python3

# stdlib
import pathlib
import shutil
import sys
import tempfile
from pydoc import getpager

# 3rd party
from domdf_python_tools.compat import importlib_resources
from domdf_python_tools.paths import PathPlus

# this package
import pyms_agilent.mhdac

__all__ = ["license_acceptor", "extract"]

EULA = """\
END-USER LICENSE TERMS

AGILENT TECHNOLOGIES, INC. SOFTWARE LICENSE TERMS
FOR THE MASSHUNTER DATA ACCESS COMPONENT RUNTIME VERSION

ATTENTION:  USE OF THE SOFTWARE IS SUBJECT TO THE LICENSE TERMS SET FORTH BELOW.

IF YOU DO NOT AGREE TO THESE LICENSE TERMS, THEN

	(A) DO NOT INSTALL OR USE THE SOFTWARE, AND
	(B) YOU MAY RETURN THE SOFTWARE FOR A FULL REFUND, OR, IF THE SOFTWARE IS
		SUPPLIED AS PART OF ANOTHER PRODUCT, YOU MAY RETURN THE ENTIRE PRODUCT
		FOR A FULL REFUND.

NOTWITHSTANDING ANYTHING TO THE CONTRARY IN THIS NOTICE, INSTALLING OR
OTHERWISE USING THE SOFTWARE INDICATES YOUR ACCEPTANCE OF THESE TERMS.


AGILENT SOFTWARE LICENSE TERMS

Software.

	'Software' means the Masshunter Data Access Component Runtime computer
	program in object code format.

License Grant.

	Agilent grants you a non-exclusive, non-transferable license to
	(a) use one copy of the Software for internal purposes in accordance with
		these License Terms and the documentation provided with the Software or
	(b) to distribute the Software for non-commercial purposes only.

	You may use one copy of the Software on one machine or instrument.
	If the software is licensed for concurrent or network use, you may not
	allow more than the maximum number of authorized users to access and use
	the software concurrently. If you distribute for non-commercial purposes
	only as permitted by this license, you must ensure that a copy of this
	license is distributed with the Software and that the recipient of the
	Software agrees to the terms of this license as a condition of execution
	of this Software.

License Restrictions.

	You may make copies or adaptations of the Software only	for archival
	purposes or only when copying or adaptation is an essential step in the
	authorized use of the Software. You must reproduce all copyright notices
	in the original Software on all permitted copies or adaptations.
	You may not copy the Software onto any public or distributed network.

Upgrades.

	This license does not entitle you to receive upgrades, updates or
	technical support. Such services may be purchased separately.

Ownership.

	The Software and all copies thereof are owned and copyrighted by Agilent.
	Agilent retains all right, title and interest in the Software.
	Agilent and its third party suppliers may protect their rights in the
	Software in the event of any violation of these License Terms.

No Disassembly.

	You may not disassemble, decompile or otherwise modify the Software
	without written authorization from Agilent, except as permitted by
	law. Upon request, you will provide Agilent with reasonably detailed
	information regarding any permitted disassembly, decompilation or
	modification.

High Risk Activities.

	The Software is not specifically designed, manufactured or intended for
	use in the planning, construction, maintenance or direct operation of a
	nuclear facility, nor for use in on line control or fail safe operation
	of aircraft navigation, control or communication systems, weapon systems
	or direct life support systems.

Termination.

	Agilent may terminate your license upon notice for breach of
	these License Terms.  Upon termination, you must immediately destroy all
	copies of the Software.

No Warranty.

	THIS SOFTWARE IS LICENSED 'AS IS' AND WITHOUT WARRANTY OF ANY KIND, EITHER
	EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES
	OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.

Limitation of Liability.

	TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT WILL AGILENT BE LIABLE FOR
	ANY LOST REVENUE, PROFIT OR DATA, OR FOR SPECIAL, INDIRECT, CONSEQUENTIAL,
	INCIDENTAL OR PUNITIVE DAMAGES, HOWEVER CAUSED REGARDLESS OF THE THEORY OF
	LIABILITY, ARISING OUT OF OR RELATED TO THE USE OF OR INABILITY TO USE
	SOFTWARE, EVEN IF AGILENT HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
	DAMAGES. In no event will Agilent's liability to you, whether in contract,
	tort (including negligence), or otherwise, exceed the amount paid by you
	for the Software. The foregoing limitations will apply even if the above
	stated warranty fails of its essential purpose.

Export Requirements.

	If you export, re-export or import Software, technology or technical data
	licensed hereunder, you assume responsibility for complying with applicable
	laws and regulations and for obtaining required export and import
	authorizations. Agilent may terminate this license immediately if you are
	in violation of any applicable laws or regulations.

U.S. Government Restricted Rights.

	Software and technical data rights granted to the federal government
	include only those rights customarily provided to end user customers.
	Agilent provides this customary commercial license in Software and
	technical data pursuant to FAR 12.211 (Technical Data) and 12.212
	(Computer Software) and, for the Department of Defense,
	DFARS 252.227-7015 (Technical Data – Commercial Items) and
	DFARS 227.7202-3 (Rights in Commercial Computer Software or Computer
	Software Documentation).

""".expandtabs(4)

x64_filenames = [
		"agtsampleinforw.dll",
		"BaseCommon.dll",
		"BaseCommon.tlb",
		"BaseDataAccess.dll",
		"BaseDataAccess.dll.config",
		"BaseDataAccess.tlb",
		"BaseError.dll",
		"BaseTof.dll",
		"MassSpecDataReader.dll",
		"MassSpecDataReader.tlb",
		"MIDAC.dll",
		]

x86_filenames = [
		"agtsampleinforw.dll",
		"agtsampleinforw.tlb",
		"BaseCommon.dll",
		"BaseCommon.tlb",
		"BaseDataAccess.dll",
		"BaseDataAccess.dll.config",
		"BaseDataAccess.tlb",
		"BaseError.dll",
		"BaseTof.dll",
		"MassSpecDataReader.dll",
		"MassSpecDataReader.tlb",
		"MIDAC.dll",
		]


def license_acceptor() -> bool:
	"""
	Shows the license and asks the user to accept it.

	:returns: Whether the user accepted the license.
	"""

	title = "Before using this software you must accept the following license:"

	pager = getpager()
	pager(f"{title}\n\n{EULA}")

	resp = input("\nIf you accept these license terms, type 'I accept' and press Enter.\n> ")

	if not resp:
		for attempt in range(10):
			resp = input("> ")
			if resp:
				break

	return resp.lower().strip() == "i accept"


def extract() -> None:
	"""
	Extract the DLL files from the zip archive.
	"""

	dest_dir = PathPlus(pyms_agilent.mhdac.__file__).parent
	(dest_dir / "x64").maybe_make()
	(dest_dir / "x86").maybe_make()

	with tempfile.TemporaryDirectory() as tmpdir:
		src_dir = pathlib.Path(tmpdir)

		with importlib_resources.path(pyms_agilent.mhdac, "mhdac.zip") as zipfile:
			shutil.unpack_archive(str(zipfile), extract_dir=src_dir, format="zip")

		for filename in x64_filenames:
			(dest_dir / "x64" / filename).write_bytes((src_dir / "x64" / filename[::-1]).read_bytes()[::-1])
		for filename in x86_filenames:
			(dest_dir / "x86" / filename).write_bytes((src_dir / "x86" / filename[::-1]).read_bytes()[::-1])


if __name__ == "__main__":
	install_dir = pathlib.Path(pyms_agilent.mhdac.__file__).parent
	if not install_dir.is_dir():
		print("Unable to determine the installation directory for pyms-agilent.")
		sys.exit(1)

	accepted = "--accept" in sys.argv or license_acceptor()

	if accepted:
		print("You have accepted the license terms.")
		extract()
		sys.exit(0)
	else:
		print("You did not accept the license.")
		sys.exit(1)
