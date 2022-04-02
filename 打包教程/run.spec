# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import pkg_resources
import os

hook_ep_packages = dict()
hiddenimports = set()

# List of packages that should have there Distutils entrypoints included.
ep_packages = ["pyocd.probe"]

if ep_packages:
    for ep_package in ep_packages:
        for ep in pkg_resources.iter_entry_points(ep_package):
            if ep_package in hook_ep_packages:
                package_entry_point = hook_ep_packages[ep_package]
            else:
                package_entry_point = []
                hook_ep_packages[ep_package] = package_entry_point
            package_entry_point.append("{} = {}:{}".format(ep.name, ep.module_name, ep.attrs[0]))
            hiddenimports.add(ep.module_name)

    try:
        os.mkdir('./generated')
    except FileExistsError:
        pass

    with open("./generated/pkg_resources_hook.py", "w") as f:
        f.write("""# Runtime hook generated from spec file to support pkg_resources entrypoints.
ep_packages = {}

if ep_packages:
    import pkg_resources
    default_iter_entry_points = pkg_resources.iter_entry_points

    def hook_iter_entry_points(group, name=None):
        if group in ep_packages and ep_packages[group]:
            eps = ep_packages[group]
            for ep in eps:
                parsedEp = pkg_resources.EntryPoint.parse(ep)
                parsedEp.dist = pkg_resources.Distribution()
                yield parsedEp
        else:
            return default_iter_entry_points(group, name)

    pkg_resources.iter_entry_points = hook_iter_entry_points
""".format(hook_ep_packages))

a = Analysis(['run.py'],
             pathex=['D:\\pro\\git\\pyocd_exe\\打包教程'],
             binaries=[],
             datas=[('D:\\ProgramData\\Miniconda3\\envs\\git_pyocd\\Lib\\site-packages\\pyocd\\debug\\svd\\svd_data.zip', '.\\pyocd\\debug\\svd\\')],
             hiddenimports=list(hiddenimports),
             hookspath=[],
             hooksconfig={},
             runtime_hooks=["./generated/pkg_resources_hook.py"],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
