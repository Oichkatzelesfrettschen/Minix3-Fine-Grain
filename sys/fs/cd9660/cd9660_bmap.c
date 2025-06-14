/*	$NetBSD: cd9660_bmap.c,v 1.5 2014/06/14 07:39:28 hannken Exp $	*/

/*-
 * Copyright (c) 1994
 *	The Regents of the University of California.  All rights reserved.
 *
 * This code is derived from software contributed to Berkeley
 * by Pace Willisson (pace@blitz.com).  The Rock Ridge Extension
 * Support code is derived from software contributed to Berkeley
 * by Atsushi Murai (amurai@spec.co.jp).
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 *	@(#)cd9660_bmap.c	8.4 (Berkeley) 12/5/94
 */

#include <sys/cdefs.h>
__KERNEL_RCSID(0, "$NetBSD: cd9660_bmap.c,v 1.5 2014/06/14 07:39:28 hannken Exp $");

#include <sys/param.h>
#include <sys/namei.h>
#include <sys/buf.h>
#include <sys/file.h>
#include <sys/vnode.h>
#include <sys/mount.h>

#include <fs/cd9660/iso.h>
#include <fs/cd9660/cd9660_extern.h>
#include <fs/cd9660/cd9660_node.h>

/**
 * Translate a file's logical block number to a physical disk block.
 *
 * The logical block is looked up in the ISO file system's extent table and
 * converted into a device block number. When provided, \a a_vpp receives the
 * underlying device vnode and \a a_bnp is set to the resulting block number.
 *
 * \param v  Pointer to a ``vop_bmap_args`` structure describing the request.
 * \return   Always returns 0.
 */
int
cd9660_bmap(void *v)
{
	struct vop_bmap_args /* {
		struct vnode *a_vp;
		daddr_t  a_bn;
		struct vnode **a_vpp;
		daddr_t *a_bnp;
		int *a_runp;
	} */ *ap = v;
	struct iso_node *ip = VTOI(ap->a_vp);
	daddr_t lblkno = ap->a_bn;
	int bshift;

	/*
	 * Check for underlying vnode requests and ensure that logical
	 * to physical mapping is requested.
	 */
	if (ap->a_vpp != NULL)
		*ap->a_vpp = ip->i_mnt->im_devvp;
	if (ap->a_bnp == NULL)
		return (0);

	/*
	 * Compute the requested block number
	 */
	bshift = ip->i_mnt->im_bshift;
	*ap->a_bnp = (ip->iso_start + lblkno) << (bshift - DEV_BSHIFT);

	/*
	 * Determine maximum number of readahead blocks following the
	 * requested block.
	 */
	if (ap->a_runp) {
		int nblk;

		nblk = (ip->i_size >> bshift) - (lblkno + 1);
		if (nblk <= 0)
			*ap->a_runp = 0;
		else if (nblk >= (MAXBSIZE >> bshift))
			*ap->a_runp = (MAXBSIZE >> bshift) - 1;
		else
			*ap->a_runp = nblk;
	}

	return (0);
}
