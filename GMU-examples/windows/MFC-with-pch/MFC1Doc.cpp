// MFC1Doc.cpp : implementation of the CMFC1Doc class
//

#include "stdafx.h"
#include "MFC1.h"

#include "MFC1Doc.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CMFC1Doc

IMPLEMENT_DYNCREATE(CMFC1Doc, CDocument)

BEGIN_MESSAGE_MAP(CMFC1Doc, CDocument)
	//{{AFX_MSG_MAP(CMFC1Doc)
		// NOTE - the ClassWizard will add and remove mapping macros here.
		//    DO NOT EDIT what you see in these blocks of generated code!
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CMFC1Doc construction/destruction

CMFC1Doc::CMFC1Doc()
{
	// TODO: add one-time construction code here

}

CMFC1Doc::~CMFC1Doc()
{
}

BOOL CMFC1Doc::OnNewDocument()
{
	if (!CDocument::OnNewDocument())
		return FALSE;

	// TODO: add reinitialization code here
	// (SDI documents will reuse this document)

	return TRUE;
}



/////////////////////////////////////////////////////////////////////////////
// CMFC1Doc serialization

void CMFC1Doc::Serialize(CArchive& ar)
{
	if (ar.IsStoring())
	{
		// TODO: add storing code here
	}
	else
	{
		// TODO: add loading code here
	}
}

/////////////////////////////////////////////////////////////////////////////
// CMFC1Doc diagnostics

#ifdef _DEBUG
void CMFC1Doc::AssertValid() const
{
	CDocument::AssertValid();
}

void CMFC1Doc::Dump(CDumpContext& dc) const
{
	CDocument::Dump(dc);
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CMFC1Doc commands
