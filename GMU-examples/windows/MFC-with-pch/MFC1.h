// MFC1.h : main header file for the MFC1 application
//

#if !defined(AFX_MFC1_H__9228F544_8424_46C2_962F_A3CDAC800221__INCLUDED_)
#define AFX_MFC1_H__9228F544_8424_46C2_962F_A3CDAC800221__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"       // main symbols

/////////////////////////////////////////////////////////////////////////////
// CMFC1App:
// See MFC1.cpp for the implementation of this class
//

class CMFC1App : public CWinApp
{
public:
	CMFC1App();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMFC1App)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation
	//{{AFX_MSG(CMFC1App)
	afx_msg void OnAppAbout();
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_MFC1_H__9228F544_8424_46C2_962F_A3CDAC800221__INCLUDED_)
